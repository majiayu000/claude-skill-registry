---
name: golang-zhiyong0804-tech-blog
description: func updateUserOnLineStatus(msg proto.Message) {
---

# code_skill

#### 判断map的key是否存在并且使用key对应的value
```
  func updateUserOnLineStatus(msg proto.Message) {
  notifyMsg := &proto.UserStatusNotifyResp{}
  err := json.Unmarshal([]byte(msg.Data), notifyMsg)

  if err != nil {
    fmt.Println(util.GetFileLine(), "updateUserOnLineStatus json unmarshal failed", err)
    return
  }

  user, ok := onlineUserMap[notifyMsg.UserId]

  if !ok {
    user = &proto.UserInfo{
      UserId: notifyMsg.UserId,
    }
  }

  user.Status = notifyMsg.Status
  onlineUserMap[notifyMsg.UserId] = user
  outPutUserOnLine()
}
```

#### redis op
```
  func (p *RedisMgr) getUser(conn redis.Conn, userId string) (user *proto.UserInfo, err error) {
	res, err := redis.String(conn.Do("Hget", UserTable, userId))

	//star_coding
	//include key not exist and user not exsit
	if err != nil {
		fmt.Println("get User err ", err)
		if err == redis.ErrNil {
			err = proto.ErrUserNotExist
		}
		return
	}

	user = &proto.UserInfo{}
	err = json.Unmarshal([]byte(res), user)

	if err != nil {
		return
	}
	return
}

func (p *RedisMgr) Login(userId string, passwd string) (user *proto.UserInfo, err error) {
	fmt.Println(util.GetFileLine() + " redis handle login")

	conn := p.pool.Get()
	defer conn.Close()

	user, err = p.getUser(conn, userId)

	if err != nil {
		return
	}

	if user.UserId != userId || user.Passwd != passwd {
		err = proto.ErrInvalidPasswd
		return
	}

	user.Status = proto.ONLINE
	user.LastLogin = util.GetTodayDateTime()
	return
}

func (p *RedisMgr) Register(user *proto.UserInfo) (err error) {
	fmt.Println(util.GetFileLine() + " redis handle register")
	conn := p.pool.Get()
	defer conn.Close()

	if user == nil {
		fmt.Println(util.GetFileLine() + "invalid user")
		err = proto.ErrInvalidParams
		return
	}

	_, err = p.getUser(conn, user.UserId)

	//has exist
	if err == nil {
		err = proto.ErrUserExist
		return
	}

	//not unregister
	if err != proto.ErrUserNotExist {
		return
	}

	data, err := json.Marshal(user)

	if err != nil {
		return
	}
	_, err = conn.Do("HSet", UserTable, user.UserId, string(data))

	if err != nil {
		return
	}
	return
}
```

#### 省去写return
```
  func (m *Map) Delete(key interface{}) {
  read, _ := m.read.Load().(readOnly)
  e, ok := read.m[key]
  if !ok && read.amended {
    m.mu.Lock()
    read, _ = m.read.Load().(readOnly)
    e, ok = read.m[key]
    if !ok && read.amended {
      delete(m.dirty, key)
    }
    m.mu.Unlock()
  }
  if ok {
    e.delete()
  }
}
```