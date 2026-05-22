---
name: wechat-integration
description: |
  基于若依-vue-plus框架的微信生态全面集成规范,覆盖小程序、公众号、企业微信等场景。
  定义微信登录授权、AccessToken管理、JS-SDK配置、消息推送、支付对接及安全防护的完整标准。
  
  触发场景:
  - 开发微信小程序登录、公众号网页授权、企业微信身份验证
  - 实现微信分享、扫一扫、地理位置等JS-SDK功能
  - 配置微信支付(小程序支付、JSAPI支付、H5支付)
  - 接收并处理微信消息推送、事件回调
  - 搭建微信生态与业务系统的用户体系打通方案
  
  触发词:微信登录、微信授权、JS-SDK、Access Token、消息推送、微信支付、OpenID、UnionID、网页授权、小程序码
---

# 微信生态集成规范

## 核心规范

### 规范1:微信登录授权流程安全

**适用场景**: 小程序登录、公众号网页授权、企业微信身份验证

**详细说明**:
1. **小程序登录流程**: 前端通过`uni.login()`获取临时登录凭证`code`(有效期5分钟),严禁在前端直接传输或存储AppSecret
2. **后端换取会话**: 后端接收`code`后,使用WxJava SDK的`wxMaService.getUserService().getSessionInfo(code)`调用微信API换取`openid`和`session_key`
3. **公众号网页授权**: 必须使用OAuth2.0重定向机制,区分静默授权(`snsapi_base`)和用户信息授权(`snsapi_userinfo`)
4. **用户体系打通**: 
   - 优先通过UnionID实现多平台统一身份(需开通微信开放平台)
   - 将OpenID与系统用户账号进行绑定,支持自动注册或手动绑定
   - 实现手机号绑定作为账号安全补充
5. **会话安全**: `session_key`仅用于解密用户敏感数据(手机号、运动数据等),严禁直接返回给前端

**技术实现**:

```java
/**
 * 微信小程序登录控制器
 * 依赖: WxJava SDK、若依权限框架
 */
@RestController
@RequestMapping("/wx/auth")
@Slf4j
public class WxAuthController {

    @Autowired
    private WxMaService wxMaService;
    
    @Autowired
    private IAuthService authService;

    /**
     * 小程序登录接口
     * @param dto 包含code、encryptedData、iv等
     * @return 系统Token和用户信息
     */
    @PostMapping("/login")
    @Anonymous // 若依注解:允许匿名访问
    public R<LoginVo> login(@Validated @RequestBody WxLoginDto dto) {
        try {
            // 1. 参数校验
            if (StringUtils.isEmpty(dto.getCode())) {
                return R.fail("登录凭证不能为空");
            }

            // 2. 换取微信会话信息(SDK自动处理AppSecret)
            WxMaJscode2SessionResult session = wxMaService.getUserService()
                .getSessionInfo(dto.getCode());
            
            String openid = session.getOpenid();
            String unionid = session.getUnionid(); // 可能为空
            String sessionKey = session.getSessionKey();

            // 3. 解密用户敏感数据(如手机号)
            String phoneNumber = null;
            if (StringUtils.isNotEmpty(dto.getEncryptedData())) {
                WxMaPhoneNumberInfo phoneInfo = wxMaService.getUserService()
                    .getPhoneNoInfo(sessionKey, dto.getEncryptedData(), dto.getIv());
                phoneNumber = phoneInfo.getPhoneNumber();
            }

            // 4. 业务层处理:绑定或注册用户,生成系统Token
            LoginVo loginVo = authService.loginByWechat(openid, unionid, phoneNumber);
            
            // 5. 记录登录日志
            AsyncManager.me().execute(AsyncFactory.recordLoginInfo(
                openid, Constants.LOGIN_SUCCESS, "微信小程序登录成功"));
            
            return R.ok(loginVo);
            
        } catch (WxErrorException e) {
            log.error("微信登录失败,错误码:{},错误信息:{}", 
                e.getError().getErrorCode(), e.getError().getErrorMsg());
            return R.fail("微信登录失败:" + e.getError().getErrorMsg());
        } catch (Exception e) {
            log.error("系统异常", e);
            return R.fail("系统繁忙,请稍后重试");
        }
    }
    
    /**
     * 公众号网页授权回调
     * @param code 授权码
     * @param state 自定义参数
     */
    @GetMapping("/mp/callback")
    public String mpCallback(@RequestParam String code, @RequestParam(required = false) String state) {
        try {
            WxMpService wxMpService = WxMpConfiguration.getMpServices().get(appId);
            WxMpOAuth2AccessToken accessToken = wxMpService.getOAuth2Service().getAccessToken(code);
            String openid = accessToken.getOpenId();
            
            // 获取用户信息(需snsapi_userinfo授权)
            WxMpUser userInfo = wxMpService.getOAuth2Service().getUserInfo(accessToken, "zh_CN");
            
            // 生成登录态并跳转
            String token = authService.loginByMpOpenId(openid, userInfo);
            return "redirect:/index.html?token=" + token;
            
        } catch (WxErrorException e) {
            log.error("网页授权失败", e);
            return "redirect:/error.html";
        }
    }
}
```

```java
/**
 * 微信登录请求DTO
 */
@Data
public class WxLoginDto {
    
    @NotBlank(message = "登录凭证不能为空")
    private String code;
    
    /** 加密数据(如手机号) */
    private String encryptedData;
    
    /** 加密算法初始向量 */
    private String iv;
    
    /** 用户昵称(小程序端获取) */
    private String nickName;
    
    /** 用户头像 */
    private String avatarUrl;
}
```

**安全要点**:
- AppSecret必须配置在后端配置文件(application-prod.yml),严禁提交到Git
- 使用Spring Cloud Config或Nacos等配置中心管理敏感配置
- session_key必须存储在服务端(Redis),设置合理过期时间(建议30天)
- 错误信息不得暴露系统内部逻辑,统一返回"登录失败,请重试"

---

### 规范2:全局AccessToken缓存与自动刷新

**适用场景**: 所有需要调用微信API的场景(消息推送、用户管理、素材管理等)

**详细说明**:
1. **缓存必要性**: 微信AccessToken每日获取次数有限(2000次),且有效期仅2小时,必须集中缓存并自动刷新
2. **缓存策略**: 
   - 使用Redis作为缓存存储,key格式:`wx:access_token:{appId}`
   - 缓存有效期设置为7000秒(略小于微信的7200秒),提前刷新避免失效
   - 使用分布式锁防止并发刷新
3. **多应用支持**: 若系统接入多个小程序或公众号,需为每个appId维护独立缓存
4. **异常处理**: 当检测到`40001`(access_token失效)错误码时,强制刷新缓存并重试

**技术实现**:

```java
/**
 * 微信配置类 - 启用Redis缓存
 */
@Configuration
@EnableConfigurationProperties(WxMaProperties.class)
public class WxMaConfiguration {

    @Autowired
    private WxMaProperties wxMaProperties;
    
    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    /**
     * 配置小程序Service - 使用Redis缓存
     */
    @Bean
    public WxMaService wxMaService() {
        WxMaDefaultConfigImpl config = new WxMaDefaultConfigImpl();
        config.setAppid(wxMaProperties.getAppId());
        config.setSecret(wxMaProperties.getAppSecret());
        
        // 核心:使用Redis存储AccessToken
        WxMaRedisConfigImpl redisConfig = new WxMaRedisConfigImpl(
            new WxRedisOps(redisTemplate), 
            "wx:ma:" + wxMaProperties.getAppId()
        );
        
        WxMaService service = new WxMaServiceImpl();
        service.setWxMaConfig(redisConfig);
        return service;
    }
    
    /**
     * 配置公众号Service - 使用Redis缓存
     */
    @Bean
    public WxMpService wxMpService() {
        WxMpRedisConfigImpl config = new WxMpRedisConfigImpl(
            new WxRedisOps(redisTemplate),
            "wx:mp:" + wxMaProperties.getMpAppId()
        );
        config.setAppId(wxMaProperties.getMpAppId());
        config.setSecret(wxMaProperties.getMpAppSecret());
        config.setToken(wxMaProperties.getMpToken());
        config.setAesKey(wxMaProperties.getMpAesKey());
        
        WxMpService service = new WxMpServiceImpl();
        service.setWxMpConfigStorage(config);
        return service;
    }
}
```

```java
/**
 * AccessToken健康检查定时任务
 * 每小时检查一次,提前预热缓存
 */
@Component
@Slf4j
public class WxAccessTokenTask {

    @Autowired
    private WxMaService wxMaService;
    
    @Autowired
    private WxMpService wxMpService;

    /**
     * 定时刷新AccessToken
     * cron: 每小时的第5分钟执行
     */
    @Scheduled(cron = "0 5 * * * ?")
    public void refreshAccessToken() {
        try {
            // 触发获取,WxJava SDK会自动判断是否需要刷新
            String maToken = wxMaService.getAccessToken(false);
            String mpToken = wxMpService.getAccessToken(false);
            
            log.info("AccessToken预热成功,小程序token:{}...,公众号token:{}...", 
                maToken.substring(0, 10), mpToken.substring(0, 10));
                
        } catch (WxErrorException e) {
            log.error("AccessToken刷新失败", e);
            // 发送告警通知(可集成企业微信机器人)
            sendAlertMessage("微信AccessToken刷新失败:" + e.getMessage());
        }
    }
}
```

**配置文件示例** (`application.yml`):

```yaml
wx:
  ma:
    app-id: wx1234567890abcdef
    app-secret: ${WX_MA_SECRET:请配置环境变量}
  mp:
    app-id: wx0987654321fedcba
    app-secret: ${WX_MP_SECRET:请配置环境变量}
    token: your_verify_token
    aes-key: your_aes_key
```

---

### 规范3:JS-SDK配置与前端调用规范

**适用场景**: 公众号H5页面调用微信能力(分享、扫码、地理位置、支付等)

**详细说明**:
1. **签名计算规则**:
   - 必须使用`jsapi_ticket`(不是access_token)
   - URL参数必须是当前页面完整URL,且去除`#`及后面的部分
   - 对于SPA应用,每次路由变化都需重新获取签名
2. **安全机制**:
   - 签名计算必须在后端完成,前端只负责接收和注入配置
   - timestamp和nonceStr需随机生成,防止重放攻击
3. **权限控制**: 根据业务需求在`jsApiList`中声明所需权限

**后端实现**:

```java
/**
 * 微信JS-SDK配置服务
 */
@Service
@Slf4j
public class WxJsApiServiceImpl implements IWxJsApiService {

    @Autowired
    private WxMpService wxMpService;

    /**
     * 获取JS-SDK配置签名
     * @param url 前端当前页面URL(必须完整,包含协议和域名)
     * @return 签名对象(包含appId、timestamp、nonceStr、signature)
     */
    @Override
    public WxJsapiSignature getJsapiSignature(String url) {
        try {
            // 1. URL预处理:去除#及后续内容
            String processedUrl = url;
            if (url.contains("#")) {
                processedUrl = url.substring(0, url.indexOf("#"));
            }
            
            // 2. 获取jsapi_ticket(SDK自动处理Redis缓存)
            String jsapiTicket = wxMpService.getJsapiTicket(true);
            
            // 3. 生成签名(SDK自动处理timestamp和nonceStr)
            WxJsapiSignature signature = wxMpService.createJsapiSignature(processedUrl);
            
            log.debug("JS-SDK签名生成成功,URL:{},signature:{}", processedUrl, signature.getSignature());
            return signature;
            
        } catch (WxErrorException e) {
            log.error("获取JS-SDK签名失败,URL:{},错误:{}", url, e.getMessage());
            throw new ServiceException("获取微信配置失败,请刷新重试");
        }
    }
    
    /**
     * 获取分享配置(包含自定义分享内容)
     */
    @Override
    public WxShareConfig getShareConfig(String url, String title, String desc, String imgUrl) {
        WxJsapiSignature signature = getJsapiSignature(url);
        
        WxShareConfig config = new WxShareConfig();
        config.setAppId(signature.getAppId());
        config.setTimestamp(signature.getTimestamp());
        config.setNonceStr(signature.getNonceStr());
        config.setSignature(signature.getSignature());
        config.setTitle(title);
        config.setDesc(desc);
        config.setLink(url);
        config.setImgUrl(imgUrl);
        
        return config;
    }
}
```

```java
/**
 * JS-SDK配置控制器
 */
@RestController
@RequestMapping("/wx/jsapi")
public class WxJsApiController {

    @Autowired
    private IWxJsApiService wxJsApiService;

    /**
     * 获取JS-SDK配置
     * @param url 前端传入的当前页面URL
     */
    @GetMapping("/config")
    public R<WxJsapiSignature> getConfig(@RequestParam String url) {
        // URL解码(防止前端编码后传输)
        String decodedUrl = URLDecoder.decode(url, StandardCharsets.UTF_8);
        
        // 安全校验:仅允许白名单域名
        if (!isAllowedDomain(decodedUrl)) {
            return R.fail("非法请求域名");
        }
        
        WxJsapiSignature signature = wxJsApiService.getJsapiSignature(decodedUrl);
        return R.ok(signature);
    }
    
    /**
     * 获取分享配置(业务接口)
     */
    @GetMapping("/share")
    public R<WxShareConfig> getShareConfig(
            @RequestParam String url,
            @RequestParam Long articleId) {
        
        // 根据文章ID查询分享内容
        Article article = articleService.getById(articleId);
        
        WxShareConfig config = wxJsApiService.getShareConfig(
            url,
            article.getTitle(),
            article.getSummary(),
            article.getCoverImage()
        );
        
        return R.ok(config);
    }
}
```

**前端调用示例** (Vue3 + Vant):

```javascript
// utils/wechat.js
import axios from 'axios';
import wx from 'weixin-js-sdk';

/**
 * 初始化微信JS-SDK
 * @param {Array} jsApiList 需要使用的API列表
 */
export async function initWxConfig(jsApiList = []) {
  const url = window.location.href.split('#')[0]; // 去除hash部分
  
  try {
    // 1. 请求后端获取签名配置
    const { data } = await axios.get('/wx/jsapi/config', {
      params: { url }
    });
    
    // 2. 注入微信配置
    wx.config({
      debug: false, // 生产环境关闭调试
      appId: data.appId,
      timestamp: data.timestamp,
      nonceStr: data.nonceStr,
      signature: data.signature,
      jsApiList: jsApiList.length > 0 ? jsApiList : [
        'updateAppMessageShareData', // 分享给朋友
        'updateTimelineShareData',    // 分享到朋友圈
        'scanQRCode',                 // 扫一扫
        'chooseImage',                // 选择图片
        'getLocation'                 // 获取地理位置
      ]
    });
    
    // 3. 等待配置就绪
    return new Promise((resolve, reject) => {
      wx.ready(() => {
        console.log('微信JS-SDK初始化成功');
        resolve(wx);
      });
      
      wx.error((err) => {
        console.error('微信JS-SDK初始化失败', err);
        reject(err);
      });
    });
    
  } catch (error) {
    console.error('获取微信配置失败', error);
    throw error;
  }
}

/**
 * 配置自定义分享内容
 * @param {Object} shareData 分享数据
 */
export async function setupShare(shareData) {
  await initWxConfig(['updateAppMessageShareData', 'updateTimelineShareData']);
  
  const config = {
    title: shareData.title,
    desc: shareData.desc,
    link: shareData.link || window.location.href,
    imgUrl: shareData.imgUrl,
    success: () => {
      console.log('分享成功');
      shareData.onSuccess?.();
    },
    cancel: () => {
      console.log('取消分享');
    }
  };
  
  // 分享给朋友
  wx.updateAppMessageShareData(config);
  
  // 分享到朋友圈(不支持desc)
  wx.updateTimelineShareData({
    title: config.title,
    link: config.link,
    imgUrl: config.imgUrl
  });
}

/**
 * 调用扫一扫
 */
export async function scanQRCode() {
  await initWxConfig(['scanQRCode']);
  
  return new Promise((resolve, reject) => {
    wx.scanQRCode({
      needResult: 1, // 返回扫码结果
      scanType: ['qrCode', 'barCode'],
      success: (res) => {
        resolve(res.resultStr);
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
}
```

**Vue组件使用示例**:

```vue
<template>
  <div class="article-detail">
    <h1>{{ article.title }}</h1>
    <div v-html="article.content"></div>
    <van-button @click="handleShare" type="primary">分享文章</van-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { setupShare } from '@/utils/wechat';
import { getArticleDetail, getShareConfig } from '@/api/article';

const article = ref({});

onMounted(async () => {
  const articleId = route.params.id;
  article.value = await getArticleDetail(articleId);
  
  // 自动配置分享
  const shareData = await getShareConfig(articleId);
  setupShare(shareData);
});

const handleShare = () => {
  // 提示用户点击右上角分享
  showToast('请点击右上角分享');
};
</script>
```

---

### 规范4:消息推送与事件回调安全验证

**适用场景**: 接收微信服务器推送的消息、事件(关注、取消关注、扫码、支付回调等)

**详细说明**:
1. **签名验证**: 必须验证微信服务器签名,防止伪造请求
2. **消息排重**: 使用消息ID去重,防止重复处理
3. **异步处理**: 微信要求5秒内响应,业务逻辑需异步处理
4. **加密模式**: 生产环境必须使用安全模式(加密传输)

**技术实现**:

```java
/**
 * 微信消息推送接收控制器
 */
@RestController
@RequestMapping("/wx/portal")
@Slf4j
public class WxPortalController {

    @Autowired
    private WxMpService wxMpService;
    
    @Autowired
    private WxMpMessageRouter messageRouter;

    /**
     * 微信服务器验证接口
     */
    @GetMapping("/mp")
    public String verify(
            @RequestParam("signature") String signature,
            @RequestParam("timestamp") String timestamp,
            @RequestParam("nonce") String nonce,
            @RequestParam("echostr") String echostr) {
        
        log.info("微信服务器验证请求,signature:{},echostr:{}", signature, echostr);
        
        // 验证签名
        if (wxMpService.checkSignature(timestamp, nonce, signature)) {
            return echostr;
        }
        
        return "非法请求";
    }

    /**
     * 接收微信消息和事件推送
     */
    @PostMapping(value = "/mp", produces = "application/xml;charset=UTF-8")
    public String receiveMessage(
            @RequestBody String requestBody,
            @RequestParam("signature") String signature,
            @RequestParam("timestamp") String timestamp,
            @RequestParam("nonce") String nonce,
            @RequestParam(value = "encrypt_type", required = false) String encryptType,
            @RequestParam(value = "msg_signature", required = false) String msgSignature) {
        
        log.info("接收微信消息推送,encryptType:{}", encryptType);
        
        // 1. 验证签名
        if (!wxMpService.checkSignature(timestamp, nonce, signature)) {
            log.error("签名验证失败");
            return "非法请求";
        }

        // 2. 解析消息
        WxMpXmlMessage inMessage;
        try {
            if ("aes".equals(encryptType)) {
                // 加密消息
                inMessage = WxMpXmlMessage.fromEncryptedXml(
                    requestBody, wxMpService.getWxMpConfigStorage(), 
                    timestamp, nonce, msgSignature
                );
            } else {
                // 明文消息(不推荐)
                inMessage = WxMpXmlMessage.fromXml(requestBody);
            }
        } catch (Exception e) {
            log.error("解析微信消息失败", e);
            return "解析失败";
        }

        // 3. 消息去重检查
        String msgId = inMessage.getMsgId() != null ? 
            String.valueOf(inMessage.getMsgId()) : inMessage.getEventKey();
        if (isDuplicateMessage(msgId)) {
            log.warn("重复消息,msgId:{}", msgId);
            return "success";
        }

        // 4. 路由消息到对应处理器
        WxMpXmlOutMessage outMessage = null;
        try {
            outMessage = messageRouter.route(inMessage);
        } catch (Exception e) {
            log.error("消息处理异常", e);
        }

        // 5. 返回响应(微信要求5秒内)
        if (outMessage == null) {
            return "success";
        }
        
        if ("aes".equals(encryptType)) {
            return outMessage.toEncryptedXml(wxMpService.getWxMpConfigStorage());
        }
        return outMessage.toXml();
    }
    
    /**
     * 消息去重检查(使用Redis)
     */
    private boolean isDuplicateMessage(String msgId) {
        if (StringUtils.isEmpty(msgId)) {
            return false;
        }
        
        String key = "wx:msg:duplicate:" + msgId;
        Boolean result = redisTemplate.opsForValue().setIfAbsent(
            key, "1", Duration.ofMinutes(5)
        );
        return !Boolean.TRUE.equals(result);
    }
}
```

```java
/**
 * 消息路由配置
 */
@Configuration
public class WxMpMessageRouterConfig {

    @Autowired
    private WxMpService wxMpService;
    
    @Autowired
    private SubscribeHandler subscribeHandler;
    
    @Autowired
    private UnsubscribeHandler unsubscribeHandler;
    
    @Autowired
    private ScanHandler scanHandler;
    
    @Autowired
    private TextMessageHandler textMessageHandler;

    @Bean
    public WxMpMessageRouter messageRouter() {
        WxMpMessageRouter router = new WxMpMessageRouter(wxMpService);
        
        // 关注事件
        router.rule()
            .async(false)
            .msgType(WxConsts.XmlMsgType.EVENT)
            .event(WxConsts.EventType.SUBSCRIBE)
            .handler(subscribeHandler)
            .end();
        
        // 取消关注事件
        router.rule()
            .async(false)
            .msgType(WxConsts.XmlMsgType.EVENT)
            .event(WxConsts.EventType.UNSUBSCRIBE)
            .handler(unsubscribeHandler)
            .end();
        
        // 扫码事件
        router.rule()
            .async(false)
            .msgType(WxConsts.XmlMsgType.EVENT)
            .event(WxConsts.EventType.SCAN)
            .handler(scanHandler)
            .end();
        
        // 文本消息(异步处理)
        router.rule()
            .async(true)
            .msgType(WxConsts.XmlMsgType.TEXT)
            .handler(textMessageHandler)
            .end();
        
        return router;
    }
}
```

```java
/**
 * 关注事件处理器示例
 */
@Component
public class SubscribeHandler implements WxMpMessageHandler {

    @Autowired
    private IUserService userService;

    @Override
    public WxMpXmlOutMessage handle(WxMpXmlMessage wxMessage,
                                     Map<String, Object> context,
                                     WxMpService wxMpService,
                                     WxSessionManager sessionManager) {
        
        String openid = wxMessage.getFromUser();
        log.info("用户关注公众号,openid:{}", openid);
        
        // 异步记录用户信息
        AsyncManager.me().execute(() -> {
            userService.recordSubscribe(openid);
        });
        
        // 返回欢迎消息
        return WxMpXmlOutMessage.TEXT()
            .content("感谢关注!回复'帮助'查看功能菜单")
            .fromUser(wxMessage.getToUser())
            .toUser(wxMessage.getFromUser())
            .build();
    }
}
```

---

### 规范5:微信支付集成规范

**适用场景**: 小程序支付、公众号JSAPI支付、H5支付、Native支付

**详细说明**:
1. **支付流程**: 统一下单 → 调起支付 → 支付回调 → 订单核验
2. **安全要点**:
   - API密钥(APIv3 Key)必须妥善保管,严禁泄露
   - 回调必须验证签名,防止伪造
   - 支付金额使用分为单位(Long类型),避免精度问题
   - 订单号必须全局唯一,建议使用雪花算法
3. **幂等性**: 支付回调可能重复推送,必须做好幂等处理

**技术实现**:

```java
/**
 * 微信支付服务(使用WxJava Payment模块)
 */
@Service
@Slf4j
public class WxPayServiceImpl implements IWxPayService {

    @Autowired
    private WxPayService wxPayService;
    
    @Autowired
    private IOrderService orderService;

    /**
     * 小程序支付统一下单
     * @param orderId 业务订单ID
     * @param userId 用户ID
     * @return 支付参数(供前端调起支付)
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public WxPayMpOrderResult createPayOrder(Long orderId, Long userId) {
        try {
            // 1. 查询订单信息
            Order order = orderService.getById(orderId);
            if (order == null || !order.getUserId().equals(userId)) {
                throw new ServiceException("订单不存在");
            }
            
            // 2. 检查订单状态
            if (!OrderStatus.UNPAID.equals(order.getStatus())) {
                throw new ServiceException("订单状态异常");
            }
            
            // 3. 获取用户OpenID
            String openid = userService.getWxOpenId(userId);
            if (StringUtils.isEmpty(openid)) {
                throw new ServiceException("请先绑定微信账号");
            }

            // 4. 构建统一下单请求
            WxPayUnifiedOrderRequest request = WxPayUnifiedOrderRequest.newBuilder()
                .outTradeNo(order.getOrderNo()) // 商户订单号(唯一)
                .body(order.getProductName())    // 商品描述
                .totalFee(order.getTotalAmount().multiply(new BigDecimal(100)).intValue()) // 金额(分)
                .spbillCreateIp(ServletUtils.getClientIP()) // 用户IP
                .notifyUrl(wxPayProperties.getNotifyUrl()) // 回调地址
                .tradeType(WxPayConstants.TradeType.JSAPI) // 交易类型
                .openid(openid) // 用户OpenID(JSAPI必需)
                .build();

            // 5. 调用统一下单API
            WxPayMpOrderResult result = wxPayService.createOrder(request);
            
            // 6. 记录支付流水
            payLogService.recordCreate(orderId, order.getOrderNo(), result);
            
            log.info("微信支付下单成功,订单号:{},prepayId:{}", 
                order.getOrderNo(), result.getPackageValue());
            
            return result;
            
        } catch (WxPayException e) {
            log.error("微信支付下单失败,orderId:{},错误码:{},错误信息:{}", 
                orderId, e.getErrCode(), e.getErrCodeDes());
            throw new ServiceException("支付下单失败:" + e.getErrCodeDes());
        }
    }

    /**
     * 处理支付回调通知
     * @param xmlData 微信推送的XML数据
     * @return 响应XML
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public String handlePayNotify(String xmlData) {
        try {
            // 1. 解析并验证签名
            WxPayOrderNotifyResult notifyResult = wxPayService.parseOrderNotifyResult(xmlData);
            
            log.info("收到支付回调,订单号:{},微信订单号:{},支付金额:{}", 
                notifyResult.getOutTradeNo(), 
                notifyResult.getTransactionId(),
                notifyResult.getTotalFee());

            // 2. 检查返回状态
            if (!WxPayConstants.ResultCode.SUCCESS.equals(notifyResult.getResultCode())) {
                log.warn("支付失败,订单号:{},失败原因:{}", 
                    notifyResult.getOutTradeNo(), notifyResult.getErrCodeDes());
                return buildSuccessResponse();
            }

            // 3. 幂等性检查:防止重复处理
            String orderNo = notifyResult.getOutTradeNo();
            if (!orderService.tryLockOrder(orderNo)) {
                log.warn("订单处理中,订单号:{}", orderNo);
                return buildSuccessResponse();
            }

            try {
                // 4. 查询订单并校验金额
                Order order = orderService.getByOrderNo(orderNo);
                if (order == null) {
                    log.error("订单不存在,订单号:{}", orderNo);
                    return buildFailResponse("订单不存在");
                }
                
                int dbAmount = order.getTotalAmount().multiply(new BigDecimal(100)).intValue();
                if (dbAmount != notifyResult.getTotalFee()) {
                    log.error("订单金额不一致,订单号:{},数据库金额:{},回调金额:{}", 
                        orderNo, dbAmount, notifyResult.getTotalFee());
                    return buildFailResponse("金额校验失败");
                }

                // 5. 更新订单状态为已支付
                orderService.updatePaid(order.getId(), notifyResult.getTransactionId());
                
                // 6. 执行业务逻辑(发货、增加积分等) - 异步处理
                AsyncManager.me().execute(() -> {
                    orderService.handlePaidOrder(order.getId());
                });
                
                // 7. 记录支付成功日志
                payLogService.recordSuccess(orderNo, notifyResult);
                
                log.info("订单支付处理完成,订单号:{}", orderNo);
                
            } finally {
                orderService.unlockOrder(orderNo);
            }

            // 8. 返回成功响应给微信
            return buildSuccessResponse();
            
        } catch (WxPayException e) {
            log.error("处理支付回调异常", e);
            return buildFailResponse("处理失败");
        }
    }
    
    /**
     * 主动查询订单支付状态
     */
    @Override
    public WxPayOrderQueryResult queryOrder(String orderNo) {
        try {
            WxPayOrderQueryRequest request = WxPayOrderQueryRequest.newBuilder()
                .outTradeNo(orderNo)
                .build();
            
            return wxPayService.queryOrder(request);
            
        } catch (WxPayException e) {
            log.error("查询订单失败,orderNo:{}", orderNo, e);
            throw new ServiceException("查询订单失败");
        }
    }
    
    /**
     * 申请退款
     */
    @Override
    public WxPayRefundResult refund(String orderNo, BigDecimal refundAmount, String reason) {
        try {
            Order order = orderService.getByOrderNo(orderNo);
            
            WxPayRefundRequest request = WxPayRefundRequest.newBuilder()
                .outTradeNo(orderNo)
                .outRefundNo("R" + orderNo) // 退款单号
                .totalFee(order.getTotalAmount().multiply(new BigDecimal(100)).intValue())
                .refundFee(refundAmount.multiply(new BigDecimal(100)).intValue())
                .refundDesc(reason)
                .notifyUrl(wxPayProperties.getRefundNotifyUrl())
                .build();
            
            WxPayRefundResult result = wxPayService.refund(request);
            
            // 记录退款流水
            payLogService.recordRefund(orderNo, result);
            
            return result;
            
        } catch (WxPayException e) {
            log.error("退款失败,orderNo:{}", orderNo, e);
            throw new ServiceException("退款失败:" + e.getErrCodeDes());
        }
    }

    private String buildSuccessResponse() {
        return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>";
    }

    private String buildFailResponse(String msg) {
        return "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[" + msg + "]]></return_msg></xml>";
    }
}
```

```java
/**
 * 支付回调控制器
 */
@RestController
@RequestMapping("/wx/pay")
public class WxPayController {

    @Autowired
    private IWxPayService wxPayService;

    /**
     * 统一下单接口
     */
    @PostMapping("/create")
    public R<WxPayMpOrderResult> createOrder(@RequestBody PayOrderDto dto) {
        Long userId = SecurityUtils.getUserId();
        WxPayMpOrderResult result = wxPayService.createPayOrder(dto.getOrderId(), userId);
        return R.ok(result);
    }

    /**
     * 支付结果回调(微信服务器调用)
     */
    @PostMapping("/notify")
    public String payNotify(@RequestBody String xmlData) {
        return wxPayService.handlePayNotify(xmlData);
    }
    
    /**
     * 退款回调
     */
    @PostMapping("/refund/notify")
    public String refundNotify(@RequestBody String xmlData) {
        return wxPayService.handleRefundNotify(xmlData);
    }
    
    /**
     * 查询订单支付状态(前端轮询)
     */
    @GetMapping("/query/{orderNo}")
    public R<String> queryOrder(@PathVariable String orderNo) {
        WxPayOrderQueryResult result = wxPayService.queryOrder(orderNo);
        
        if (WxPayConstants.TradeState.SUCCESS.equals(result.getTradeState())) {
            return R.ok("SUCCESS");
        } else if (WxPayConstants.TradeState.NOTPAY.equals(result.getTradeState())) {
            return R.ok("NOTPAY");
        } else {
            return R.ok("FAIL");
        }
    }
}
```

**前端调起支付** (uni-app):

```javascript
// api/payment.js
export function createWxPayOrder(orderId) {
  return request({
    url: '/wx/pay/create',
    method: 'post',
    data: { orderId }
  });
}

export function queryPayStatus(orderNo) {
  return request({
    url: `/wx/pay/query/${orderNo}`,
    method: 'get'
  });
}

// pages/payment/index.vue
import { createWxPayOrder, queryPayStatus } from '@/api/payment';

async function handlePay() {
  try {
    uni.showLoading({ title: '正在拉起支付...' });
    
    // 1. 请求后端下单
    const payData = await createWxPayOrder(orderId);
    
    // 2. 调起微信支付
    uni.requestPayment({
      provider: 'wxpay',
      timeStamp: payData.timeStamp,
      nonceStr: payData.nonceStr,
      package: payData.packageValue,
      signType: payData.signType,
      paySign: payData.paySign,
      success: async (res) => {
        uni.showToast({ title: '支付成功', icon: 'success' });
        
        // 3. 轮询查询支付状态(备用方案)
        await checkPayStatus(orderNo);
      },
      fail: (err) => {
        if (err.errMsg.includes('cancel')) {
          uni.showToast({ title: '已取消支付', icon: 'none' });
        } else {
          uni.showToast({ title: '支付失败', icon: 'none' });
        }
      }
    });
    
  } catch (error) {
    console.error('支付异常', error);
    uni.showToast({ title: error.message || '支付失败', icon: 'none' });
  } finally {
    uni.hideLoading();
  }
}

// 轮询查询支付状态
async function checkPayStatus(orderNo, maxRetry = 5) {
  for (let i = 0; i < maxRetry; i++) {
    await new Promise(resolve => setTimeout(resolve, 2000)); // 等待2秒
    
    const status = await queryPayStatus(orderNo);
    if (status === 'SUCCESS') {
      // 跳转到订单详情页
      uni.navigateTo({ url: `/pages/order/detail?orderNo=${orderNo}` });
      return;
    }
  }
}
```

---

## 禁止事项

### 1. 安全禁令(Security Prohibitions)

- ❌ **严禁在前端代码中硬编码AppSecret**: 
  - 包括Vue/React/uni-app等任何前端代码、config.js配置文件、小程序的app.js等
  - AppSecret泄露将导致微信账号完全失控,可被任意调用API
  
- ❌ **严禁将AppSecret提交到Git仓库**:
  - 必须配置`.gitignore`忽略配置文件或使用环境变量
  - 如已提交,必须立即在微信公众平台重置AppSecret并删除Git历史记录

- ❌ **严禁将session_key直接返回给前端**:
  - session_key仅用于服务端解密用户敏感数据(手机号、运动数据等)
  - 必须存储在服务端(Redis),并关联到业务系统的登录态

- ❌ **严禁在处理微信回调时不验证签名**:
  - 所有消息推送、支付回调、退款回调必须验证签名
  - 必须检查`return_code`和`result_code`双重状态

- ❌ **严禁在生产环境使用明文模式接收消息**:
  - 公众号必须配置为"安全模式(推荐)",使用AES加密消息
  - Token和EncodingAESKey必须定期更换

### 2. 性能禁令(Performance Prohibitions)

- ❌ **严禁每次调用API都重新获取AccessToken**:
  - 微信AccessToken每日获取上限2000次,频繁获取将被封禁
  - 必须使用Redis等缓存,有效期设置为7000秒

- ❌ **严禁不使用缓存存储JsapiTicket**:
  - JsapiTicket每日获取上限同样有限制
  - WxJava SDK默认支持Redis缓存,必须正确配置

- ❌ **严禁在同步流程中处理耗时业务逻辑**:
  - 微信要求消息回调5秒内响应,超时会重复推送
  - 必须立即返回"success",业务逻辑使用异步任务处理

### 3. 业务禁令(Business Prohibitions)

- ❌ **严禁不做订单幂等性处理**:
  - 支付回调可能重复推送(网络抖动、超时等)
  - 必须使用分布式锁或数据库唯一索引保证幂等

- ❌ **严禁使用浮点数处理支付金额**:
  - 必须使用`BigDecimal`或整型(分为单位)
  - 示例:订单金额99.99元,传给微信的totalFee应为9999(分)

- ❌ **严禁支付回调不校验金额**:
  - 必须对比回调金额与数据库订单金额是否一致
  - 防止用户篡改支付金额的攻击

- ❌ **严禁在JS-SDK签名中使用错误的URL**:
  - 必须使用当前页面完整URL(包含协议和域名)
  - 必须去除`#`及后面的hash部分
  - SPA应用路由变化后需重新获取签名

### 4. 数据禁令(Data Prohibitions)

- ❌ **严禁不做消息去重处理**:
  - 微信可能推送重复消息,必须根据MsgId去重
  - 使用Redis Set存储已处理的MsgId,过期时间5分钟

- ❌ **严禁在日志中打印完整的AccessToken和AppSecret**:
  - 日志只能打印前10位,例如:`token: a1b2c3d4e5...`
  - 避免日志泄露导致安全风险

- ❌ **严禁不处理UnionID**:
  - 如有多个小程序或公众号,必须通过UnionID实现用户统一
  - 需在微信开放平台绑定应用才能获取UnionID

### 5. 错误处理禁令(Error Handling Prohibitions)

- ❌ **严禁忽略微信错误码**:
  - 必须根据错误码做针对性处理(如40001自动刷新token)
  - 常见错误码:40001(token失效)、41001(缺少access_token)、42001(token超时)

- ❌ **严禁直接暴露微信错误信息给用户**:
  - 用户端应显示友好提示,如"网络繁忙,请稍后重试"
  - 详细错误信息记录到日志,便于排查

- ❌ **严禁不配置微信API调用失败告警**:
  - 应配置企业微信/钉钉机器人,AccessToken获取失败时立即告警
  - 监控支付回调失败率,及时发现异常

---

## 技术栈与依赖

### 1. 后端依赖(Maven)

```xml
<!-- WxJava 微信开发SDK -->
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>weixin-java-mp</artifactId> <!-- 公众号 -->
    <version>4.6.0</version>
</dependency>

<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>weixin-java-miniapp</artifactId> <!-- 小程序 -->
    <version>4.6.0</version>
</dependency>

<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>weixin-java-pay</artifactId> <!-- 支付 -->
    <version>4.6.0</version>
</dependency>

<!-- Redis支持(AccessToken缓存) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

### 2. 前端依赖

**小程序(uni-app)**:
```json
{
  "dependencies": {
    "weixin-js-sdk": "^1.6.0"
  }
}
```

**公众号H5(Vue3)**:
```bash
npm install weixin-js-sdk
```

### 3. 配置文件结构

```
application.yml
├── wx.ma (小程序配置)
│   ├── app-id
│   ├── app-secret (使用环境变量)
│   └── token
├── wx.mp (公众号配置)
│   ├── app-id
│   ├── app-secret
│   ├── token
│   └── aes-key
└── wx.pay (支付配置)
    ├── mch-id (商户号)
    ├── mch-key (APIv3密钥)
    ├── notify-url (回调地址)
    └── cert-path (证书路径,用于退款)
```

---

## 参考代码

### 项目文件路径

**后端(若依-vue-plus框架)**:
```
ruoyi-admin/
└── src/main/java/com/ruoyi/
    ├── web/controller/wx/
    │   ├── WxAuthController.java          # 微信登录控制器
    │   ├── WxJsApiController.java         # JS-SDK配置控制器
    │   ├── WxPayController.java           # 支付控制器
    │   └── WxPortalController.java        # 消息推送接收控制器
    ├── service/
    │   ├── IWxJsApiService.java           # JS-SDK服务接口
    │   ├── IWxPayService.java             # 支付服务接口
    │   └── impl/
    │       ├── WxJsApiServiceImpl.java
    │       └── WxPayServiceImpl.java
    └── config/
        ├── WxMaConfiguration.java         # 小程序配置类
        ├── WxMpConfiguration.java         # 公众号配置类
        ├── WxPayConfiguration.java        # 支付配置类
        └── WxMpMessageRouterConfig.java   # 消息路由配置
```

**前端(uni-app)**:
```
src/
├── api/
│   ├── auth.js                  # 登录接口
│   └── payment.js               # 支付接口
├── utils/
│   └── wechat.js                # 微信能力封装(JS-SDK初始化、分享等)
└── pages/
    ├── login/index.vue          # 登录页
    └── payment/index.vue        # 支付页
```

---

## 检查清单

### 开发阶段检查

- [ ] **登录流程**
  - [ ] 前端是否使用`uni.login()`获取code(不涉及AppSecret)
  - [ ] 后端是否通过WxJava SDK换取OpenID和session_key
  - [ ] 是否实现了OpenID与系统用户的绑定逻辑
  - [ ] 是否支持UnionID跨应用用户统一(如有多个小程序/公众号)
  - [ ] session_key是否存储在服务端(Redis),未返回给前端

- [ ] **AccessToken管理**
  - [ ] 是否配置了Redis作为缓存存储
  - [ ] WxJava配置类是否正确使用`WxMaRedisConfigImpl`/`WxMpRedisConfigImpl`
  - [ ] 缓存key是否包含appId前缀,防止多应用冲突
  - [ ] 是否配置了定时任务预热AccessToken(建议每小时执行一次)
  - [ ] 是否配置了AccessToken获取失败的告警通知

- [ ] **JS-SDK配置**
  - [ ] 签名计算是否在后端完成
  - [ ] 是否正确处理URL(去除#及后续内容)
  - [ ] 前端是否在每次路由变化后重新获取签名(SPA应用)
  - [ ] 是否配置了JS接口安全域名(微信公众平台设置)
  - [ ] 分享配置的link和imgUrl是否使用完整URL(包含协议)

- [ ] **消息推送**
  - [ ] 是否验证微信服务器签名
  - [ ] 是否使用安全模式(AES加密)接收消息
  - [ ] 是否实现了消息去重逻辑(基于MsgId)
  - [ ] 业务逻辑是否异步处理(5秒内返回响应)
  - [ ] 是否正确配置了消息推送URL和Token(微信公众平台)

- [ ] **支付对接**
  - [ ] 订单号是否全局唯一(建议使用雪花算法)
  - [ ] 金额是否使用分为单位(整型或BigDecimal)
  - [ ] 是否实现了支付回调的签名验证
  - [ ] 是否校验了回调金额与订单金额的一致性
  - [ ] 是否实现了幂等性处理(分布式锁或数据库唯一索引)
  - [ ] 是否配置了支付回调URL和退款回调URL
  - [ ] 商户证书是否正确配置(用于退款API)

### 安全检查

- [ ] **配置安全**
  - [ ] AppSecret是否配置为环境变量或加密存储
  - [ ] `.gitignore`是否包含配置文件(如`application-prod.yml`)
  - [ ] 生产环境配置是否使用配置中心(Nacos/Apollo)

- [ ] **代码安全**
  - [ ] 前端代码是否完全不包含AppSecret
  - [ ] 日志是否打印完整的AccessToken或AppSecret
  - [ ] 敏感错误信息是否直接暴露给用户

- [ ] **接口安全**
  - [ ] 支付接口是否需要登录鉴权
  - [ ] JS-SDK配置接口是否限制了域名白名单
  - [ ] 消息推送接口是否验证了微信服务器IP

### 上线前检查

- [ ] **微信公众平台配置**
  - [ ] 服务器域名配置:request合法域名、uploadFile合法域名、downloadFile合法域名
  - [ ] 业务域名配置(公众号H5页面)
  - [ ] JS接口安全域名配置
  - [ ] 消息推送URL配置并完成Token验证
  - [ ] 支付授权目录配置

- [ ] **性能优化**
  - [ ] Redis缓存是否生效(查看日志确认未频繁调用微信API)
  - [ ] 是否配置了连接池(Lettuce/Jedis)
  - [ ] 异步任务是否配置了合理的线程池大小

- [ ] **监控告警**
  - [ ] AccessToken获取失败告警
  - [ ] 支付回调失败率监控
  - [ ] 消息推送处理异常告警
  - [ ] 微信API调用QPS和耗时监控

### 测试检查

- [ ] **功能测试**
  - [ ] 小程序登录完整流程测试
  - [ ] 公众号网页授权流程测试
  - [ ] JS-SDK各功能测试(分享、扫码、地理位置等)
  - [ ] 支付全流程测试(下单、支付、回调、查询、退款)

- [ ] **异常测试**
  - [ ] 网络超时、微信服务器异常的降级处理
  - [ ] AccessToken失效时的自动刷新
  - [ ] 支付回调重复推送的幂等性
  - [ ] 订单金额篡改的安全校验

- [ ] **压力测试**
  - [ ] 高并发下AccessToken缓存是否正常
  - [ ] 支付回调并发处理是否有锁竞争问题
  - [ ] Redis连接池是否够用

---

## 常见问题与解决方案

### Q1: 小程序登录提示"code已被使用"

**原因**: code只能使用一次,有效期5分钟,重复调用会报错

**解决方案**:
```javascript
// 前端:每次登录都重新获取code
async login() {
  const { code } = await uni.login();
  const res = await api.wxLogin({ code }); // 立即发送到后端
  uni.setStorageSync('token', res.token);
}
```

### Q2: JS-SDK配置提示"invalid signature"

**原因**:
1. URL处理不正确(未去除#)
2. 使用了错误的ticket(应该用jsapi_ticket而非access_token)
3. 前端使用的URL与传给后端的URL不一致

**解决方案**:
```javascript
// 正确获取URL
const url = window.location.href.split('#')[0];

// 前端完整调用示例
import { initWxConfig } from '@/utils/wechat';

// 在Vue mounted或onMounted中调用
onMounted(() => {
  initWxConfig(['updateAppMessageShareData']).then(() => {
    console.log('微信JS-SDK初始化成功');
  });
});
```

### Q3: 支付成功但订单状态未更新

**原因**:
1. 支付回调接口异常,微信推送失败
2. 回调处理逻辑有bug,事务回滚
3. 服务器防火墙拦截了微信回调

**解决方案**:
```java
// 1. 检查回调接口日志
log.info("收到支付回调,订单号:{}", notifyResult.getOutTradeNo());

// 2. 前端主动轮询查询支付状态(兜底方案)
async checkPayStatus(orderNo) {
  for (let i = 0; i < 5; i++) {
    await sleep(2000);
    const status = await queryPayStatus(orderNo);
    if (status === 'SUCCESS') {
      // 跳转订单详情
      return;
    }
  }
}

// 3. 配置服务器安全组,放行微信回调IP段
// 微信支付IP段: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=23_2
```

### Q4: AccessToken频繁失效

**原因**:
1. Redis缓存未生效,每次都重新获取
2. 多个服务器实例未共享缓存
3. Redis缓存过期时间设置不当

**解决方案**:
```java
// 1. 确认Redis配置生效
@Bean
public WxMaService wxMaService(RedisTemplate<String, String> redisTemplate) {
    WxMaRedisConfigImpl config = new WxMaRedisConfigImpl(
        new WxRedisOps(redisTemplate),
        "wx:ma:" + appId
    );
    // 配置...
    return service;
}

// 2. 查看Redis中是否有缓存key
redis-cli keys "wx:*"

// 3. 检查日志,确认未频繁调用微信API
log.debug("从缓存获取AccessToken");
```

### Q5: 公众号网页授权提示"redirect_uri参数错误"

**原因**: 微信公众平台未配置回调域名或配置错误

**解决方案**:
1. 登录微信公众平台
2. 进入"设置与开发" → "公众号设置" → "功能设置"
3. 配置"网页授权域名"(不包含http://和路径)
4. 下载验证文件并放到网站根目录

```
配置示例:
域名: www.example.com
回调地址: https://www.example.com/wx/auth/mp/callback
```

### Q6: 消息推送一直收不到

**原因**:
1. 服务器配置错误,Token验证失败
2. 服务器未正确响应"GET请求验证"
3. 生产环境未使用80或443端口

**解决方案**:
```java
// 1. 实现GET请求验证接口
@GetMapping("/wx/portal/mp")
public String verify(@RequestParam String signature,
                     @RequestParam String timestamp,
                     @RequestParam String nonce,
                     @RequestParam String echostr) {
    if (wxMpService.checkSignature(timestamp, nonce, signature)) {
        return echostr; // 必须原样返回
    }
    return "非法请求";
}

// 2. 微信公众平台配置示例
URL: https://www.example.com/wx/portal/mp
Token: 自定义(与配置文件一致)
EncodingAESKey: 随机生成(43位)
消息加解密方式: 安全模式(推荐)
```

---

## 高级特性

### 1. 小程序订阅消息(替代模板消息)

```java
/**
 * 发送订阅消息
 */
public void sendSubscribeMessage(String openid, String orderId) {
    try {
        WxMaSubscribeMessage message = WxMaSubscribeMessage.builder()
            .toUser(openid)
            .templateId("模板ID") // 从微信公众平台获取
            .page("pages/order/detail?id=" + orderId)
            .data(List.of(
                new WxMaSubscribeMessage.MsgData("thing1", "订单已发货"),
                new WxMaSubscribeMessage.MsgData("character_string2", orderId),
                new WxMaSubscribeMessage.MsgData("date3", DateUtils.formatNow())
            ))
            .build();
        
        wxMaService.getMsgService().sendSubscribeMsg(message);
        log.info("订阅消息发送成功,openid:{}", openid);
        
    } catch (WxErrorException e) {
        log.error("订阅消息发送失败,errcode:{}", e.getError().getErrorCode());
    }
}
```

### 2. 生成小程序码

```java
/**
 * 生成小程序码(无限制数量)
 */
public byte[] generateUnlimitQrCode(String scene, String page) {
    try {
        WxMaCodeLineColor lineColor = new WxMaCodeLineColor("0", "0", "0");
        
        byte[] qrCodeBytes = wxMaService.getQrcodeService().createWxaCodeUnlimitBytes(
            scene,      // 参数(最多32个字符)
            page,       // 跳转页面
            false,      // 是否需要透明底色
            "release",  // 环境版本
            430,        // 二维码宽度
            true,       // 是否需要圆角
            lineColor,  // 线条颜色
            false       // 是否带logo
        );
        
        return qrCodeBytes;
        
    } catch (WxErrorException e) {
        log.error("生成小程序码失败", e);
        throw new ServiceException("生成小程序码失败");
    }
}
```

### 3. 微信客服消息(48小时内主动推送)

```java
/**
 * 发送客服消息(文本)
 */
public void sendCustomMessage(String openid, String content) {
    try {
        WxMaKefuMessage message = WxMaKefuMessage.newTextBuilder()
            .toUser(openid)
            .content(content)
            .build();
        
        wxMaService.getMsgService().sendKefuMsg(message);
        
    } catch (WxErrorException e) {
        log.error("客服消息发送失败", e);
    }
}

/**
 * 发送客服消息(图片)
 */
public void sendImageMessage(String openid, String mediaId) {
    WxMaKefuMessage message = WxMaKefuMessage.newImageBuilder()
        .toUser(openid)
        .mediaId(mediaId)
        .build();
    
    wxMaService.getMsgService().sendKefuMsg(message);
}
```

### 4. 获取用户手机号(需用户主动授权)

```java
/**
 * 解密手机号(小程序button open-type="getPhoneNumber")
 */
@PostMapping("/getPhone")
public R<String> getPhoneNumber(@RequestBody PhoneDto dto) {
    try {
        // 从Redis获取session_key
        String sessionKey = redisTemplate.opsForValue().get("wx:session:" + userId);
        
        // 解密手机号
        WxMaPhoneNumberInfo phoneInfo = wxMaService.getUserService().getPhoneNoInfo(
            sessionKey,
            dto.getEncryptedData(),
            dto.getIv()
        );
        
        String phoneNumber = phoneInfo.getPhoneNumber();
        
        // 绑定手机号到用户账号
        userService.bindPhone(userId, phoneNumber);
        
        return R.ok(phoneNumber);
        
    } catch (Exception e) {
        log.error("获取手机号失败", e);
        return R.fail("获取手机号失败");
    }
}
```

---

## 性能优化建议

### 1. AccessToken预加载策略

```java
/**
 * 应用启动时预加载AccessToken
 */
@Component
public class WxAccessTokenPreloader implements ApplicationRunner {

    @Autowired
    private WxMaService wxMaService;

    @Override
    public void run(ApplicationArguments args) throws Exception {
        try {
            // 提前获取token,触发缓存
            wxMaService.getAccessToken(false);
            log.info("微信AccessToken预加载成功");
        } catch (Exception e) {
            log.error("AccessToken预加载失败", e);
        }
    }
}
```

### 2. 消息推送异步处理

```java
/**
 * 消息处理器使用异步线程池
 */
@Component
public class AsyncMessageHandler implements WxMpMessageHandler {

    @Autowired
    @Qualifier("wxMsgExecutor")
    private ThreadPoolTaskExecutor executor;

    @Override
    public WxMpXmlOutMessage handle(WxMpXmlMessage wxMessage, ...) {
        // 立即返回,业务逻辑异步处理
        executor.execute(() -> {
            processMessage(wxMessage);
        });
        
        return null; // 返回null表示success
    }
}

// 配置专用线程池
@Bean("wxMsgExecutor")
public ThreadPoolTaskExecutor wxMessageExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(5);
    executor.setMaxPoolSize(10);
    executor.setQueueCapacity(100);
    executor.setThreadNamePrefix("wx-msg-");
    executor.initialize();
    return executor;
}
```

### 3. JS-SDK签名结果缓存(SPA应用)

```javascript
// 前端缓存签名结果(同一URL不重复请求)
const signatureCache = new Map();

export async function initWxConfig(jsApiList = []) {
  const url = getCleanUrl();
  
  // 检查缓存
  if (signatureCache.has(url)) {
    const cachedConfig = signatureCache.get(url);
    wx.config({ ...cachedConfig, jsApiList });
    return;
  }
  
  // 请求后端获取签名
  const signature = await getSignature(url);
  signatureCache.set(url, signature);
  
  wx.config({ ...signature, jsApiList });
}
```

---

## 总结

本SKILL文档定义了基于若依-vue-plus框架的微信生态集成完整规范,涵盖:

1. **登录授权**: 小程序登录、公众号网页授权、UnionID用户统一
2. **缓存策略**: AccessToken和JsapiTicket的Redis缓存与自动刷新
3. **JS-SDK**: 签名计算、前端调用、常见API封装
4. **消息推送**: 签名验证、消息去重、异步处理、加密模式
5. **支付对接**: 统一下单、支付回调、金额校验、幂等性处理
6. **安全规范**: AppSecret保护、回调验证、错误处理、日志脱敏
7. **性能优化**: 缓存预加载、异步处理、连接池配置
8. **常见问题**: 典型错误场景与解决方案

遵循本规范可确保微信集成的**安全性、稳定性和可维护性**,避免常见的坑点和安全隐患。

---

## 参考文档

- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [微信公众平台技术文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [微信支付API文档](https://pay.weixin.qq.com/wiki/doc/api/index.html)
- [WxJava SDK文档](https://github.com/Wechat-Group/WxJava/wiki)
- [若依-vue-plus文档](http://doc.vueplus.org/)
