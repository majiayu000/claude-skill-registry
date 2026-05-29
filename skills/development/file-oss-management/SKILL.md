---
name: file-oss-management
description: |
  基于若依-vue-plus框架，定义文件上传与对象存储（OSS）集成的标准规范。涵盖统一上传接口封装、文件安全性校验（类型/大小/路径）、重命名策略及多端组件使用标准。
  触发场景：在开发头像上传、附件下载、Excel导入导出或配置MinIO/阿里云OSS时。
  触发词：文件上传、OSS集成、图片上传、MinIO配置、文件安全
---

# 文件上传与 OSS 管理规范

## 核心规范
### 规范1：统一上传接口与 OSS 配置
（详细说明：必须使用若依封装的 `SysOssController` 或自定义 `UploadController` 处理文件上传。底层应支持多种存储策略（本地、MinIO、阿里云OSS、腾讯云COS等），通过配置文件 `ruoyi.profile` 或数据库动态切换。Controller 层需使用 `@RepeatSubmit` 注解防止重复提交。）

```java
@RestController
@RequestMapping("/system/oss")
public class SysOssController extends BaseController {

    @Autowired
    private ISysOssService sysOssService;

    /**
     * 统一文件上传接口
     */
    @PreSaCheckPermissionAuthorize("system:oss:upload")
    @Log(title = "OSS文件上传", businessType = BusinessType.INSERT)
    @RepeatSubmit(interval = 3000) // 3秒内防重复提交
    @PostMapping("/upload")
    public R<Map<String, String>> upload(@RequestPart("file") MultipartFile file) {
        if (file.isEmpty()) {
            return R.fail("上传文件不能为空");
        }
        
        try {
            // 调用Service层上传，返回访问URL和文件ID
            SysOss oss = sysOssService.upload(file);
            
            Map<String, String> result = new HashMap<>();
            result.put("url", oss.getUrl());
            result.put("fileName", oss.getFileName());
            result.put("ossId", oss.getOssId().toString());
            
            return R.ok(result);
        } catch (Exception e) {
            log.error("文件上传失败", e);
            return R.fail(e.getMessage());
        }
    }
}
```

### 规范2：文件安全校验与重命名策略
（详细说明：严禁信任用户提交的原始文件名。必须使用 `FileUploadUtils` 工具类进行文件上传，该工具类内置了后缀白名单校验（防止上传.jsp、.exe等脚本文件）、文件大小限制及UUID重命名逻辑。对于本地存储，需确保上传目录位于WebRoot之外或不可执行路径下。）

```java
@Service
public class SysOssServiceImpl implements ISysOssService {

    /**
     * 本地文件上传核心逻辑示例
     */
    @Override
    public SysOss uploadLocal(MultipartFile file) {
        // 1. 校验文件扩展名（内部基于白名单机制）
        // 2. 校验文件大小（默认配置上限）
        String fileName = FileUploadUtils.upload(RuoYiConfig.getUploadPath(), file);
        
        String url = serverConfig.getUrl() + fileName;
        
        SysOss oss = new SysOss();
        oss.setFileName(FileUtils.getName(fileName));
        oss.setOriginalName(file.getOriginalFilename());
        oss.setFileSuffix(FileUtils.getExtension(fileName));
        oss.setUrl(url);
        // ...保存到数据库
        return baseMapper.insert(oss);
    }
    
    // 对于OSS上传，同样建议先校验后上传
    public void validateFile(MultipartFile file) {
        // 校验扩展名
        String extension = FileUploadUtils.getExtension(file);
        if (!FileUploadUtils.isAllowedExtension(extension, MimeTypeUtils.DEFAULT_ALLOWED_EXTENSION)) {
            throw new ServiceException("文件格式不正确，请上传" + Arrays.toString(MimeTypeUtils.DEFAULT_ALLOWED_EXTENSION) + "格式");
        }
    }
}
```

## 禁止事项
- ❌ 禁止直接使用 `file.getOriginalFilename()` 作为服务器存储文件名（必须使用UUID重命名）。
- ❌ 禁止上传可执行文件（如 .exe, .sh, .jsp, .php）到可执行目录，必须在 `application.yml` 中配置 `allowed-extension` 黑/白名单。
- ❌ 禁止在文件上传接口中省略文件大小限制，防止恶意大文件攻击导致磁盘溢出。
- ❌ 禁止将文件直接存储在项目 `src/main/resources` 或 `static` 目录下（推荐存储在外部目录或OSS）。
- ❌ 禁止在前端URL中携带本地绝对路径，文件访问必须通过服务器流或OSS签名URL。

## 参考代码
- 文件路径：`ruoyi-admin/src/main/java/com/ruoyi/web/controller/system/SysOssController.java`
- 文件路径：`ruoyi-common/src/main/java/com/ruoyi/common/utils/file/FileUploadUtils.java`
- 文件路径：`ruoyi-ui/src/components/ImageUpload/index.vue`（前端上传组件）

## 检查清单
- [ ] 是否遵循统一的上传接口标准
- [ ] 是否配置了正确的文件后缀白名单
- [ ] 是否使用了UUID或时间戳重命名文件
- [ ] 是否在接口上添加了防重复提交注解
- [ ] 是否限制了单次上传文件的最大大小