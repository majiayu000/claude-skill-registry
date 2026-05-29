# skill
----
    import "mind/core/framework/skill"

Package skill provides an interface to be implemented by the robot part of a
Skill.

This function must be implemented in your skill package:

    func NewSkill() skill.Interface

## Usage

#### func  SkillDataPath

```go
func SkillDataPath() (string, error)
```
Get skill's data path on robot.

#### type Base

```go
type Base struct{}
```

struct Base implements the base Skill interface

#### func (*Base) OnClose

```go
func (b *Base) OnClose()
```

#### func (*Base) OnConnect

```go
func (b *Base) OnConnect()
```

#### func (*Base) OnDisconnect

```go
func (b *Base) OnDisconnect()
```

#### func (*Base) OnRecvJSON

```go
func (b *Base) OnRecvJSON(data []byte)
```

#### func (*Base) OnRecvString

```go
func (b *Base) OnRecvString(data string)
```

#### func (*Base) OnStart

```go
func (b *Base) OnStart()
```

#### type Interface

```go
type Interface interface {
	OnStart()            // Called when Skill is started.
	OnConnect()          // OnConnect is called when robot has connected to remote.
	OnClose()            // OnClose is called when Skill is closed. You have 1 second to do clean up before Skill is force terminated.
	OnRecvJSON([]byte)   // OnRecvJSON is called when remote send JSON data to robot. Use json.Unmarshal to parse.
	OnRecvString(string) // OnRecvString will be called when remote send string data ro robot.
	OnDisconnect()       // OnDisconnect is called when remote disconnected from robot.
}
```

Interface must be implemented in every skill.

#### type Robotinfo

```go
type Robotinfo struct {
	Battery     float32 `json:"battery"`     // Battery is during 0~1 and 1 means the battery is full of power.
	Temperature float32 `json:"temperature"` // The unit of temperature is centigrade.
	DiskSpace   uint64  `json:"disk_space"`  // The unit of diskspace is byte(B).
	IsCharging  bool    `json:"is_charging"`
	SN          string  `json:"sn"`
	Nickname    string  `json:"nickname"`
	Owner       string  `json:"owner"`
	Version     string  `json:"version"`
}
```

Robotinfo is the information of robot.

#### func  RobotInfo

```go
func RobotInfo() (Robotinfo, error)
```
Function RobotInfo is used to get the robot's information.
