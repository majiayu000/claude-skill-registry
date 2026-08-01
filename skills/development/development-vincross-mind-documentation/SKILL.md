---
name: development-vincross-mind-documentation
description: You can find the MoveLegsSkill example code on our GitHub. Here are some
  annotated notes about the implementation and reference to help you build your own
  Skills.
---

# MoveLegsSkill

You can find the MoveLegsSkill example code on our [GitHub](https://github.com/vincross/mind-sdk/blob/master/examples/MoveLegsSkill/robot/src/movelegsskill.go). Here are some annotated notes about the implementation and reference to help you build your own Skills.

# ready\(\) function

```go
func ready() {
	hexabody.Stand()
	hexabody.MoveHead(0.0, FAST_DURATION)
	// Using goroutines to make some commands be executed at the same time
	go hexabody.MoveLeg(2, hexabody.NewLegPosition().SetCoordinates(-100, 50.0, 70.0), SLOW_DURATION)
	hexabody.MoveLeg(5, hexabody.NewLegPosition().SetCoordinates(100, 50.0, 70.0), SLOW_DURATION)
	go hexabody.MoveJoint(0, 1, 90, SLOW_DURATION)
	hexabody.MoveJoint(0, 2, 45, SLOW_DURATION)
	go hexabody.MoveJoint(1, 1, 90, FAST_DURATION)
	hexabody.MoveJoint(1, 2, 45, FAST_DURATION)
}
```

This `ready()` function tells HEXA to stand, move its head to the default position, and move its legs into a starting position.

```go
go hexabody.MoveLeg(2, hexabody.NewLegPosition().SetCoordinates(-100, 50.0, 70.0), SLOW_DURATION)
hexabody.MoveLeg(5, hexabody.NewLegPosition().SetCoordinates(100, 50.0, 70.0), SLOW_DURATION)
```

Let's go through these lines more in detail. From the API Reference, we see that the format for `MoveLeg` is:

```
func MoveLeg(legNumber int, legPosition *LegPosition, duration int) error
```

So the first argument refers to the leg number. We can tell from the diagram on the [Hardware](/Introduction/hardware.md) page that legs 2 and 5 refer to the left and right legs. Now that we know what legs to move, we tell HEXA to create a new leg position using the coordinates provided. You can find more information about how coordinates are set up on the [Hardware](/Introduction/hardware.md) page as well.

Next, we need to move the joints in the front two legs to a default position for stability.

```go
go hexabody.MoveJoint(0, 1, 90, SLOW_DURATION)
hexabody.MoveJoint(0, 2, 45, SLOW_DURATION)
go hexabody.MoveJoint(1, 1, 90, FAST_DURATION)
hexabody.MoveJoint(1, 2, 45, FAST_DURATION)
```

The `MoveJoint` format looks like this:

```go
func MoveJoint(legNumber, jointNumber int, degree float64, duration int) error
```

So that means we are going to move _legs 0 and 1_, and _joints 1 and 2_ of those legs to 90 and 45 degrees, respectively. You can see an example of the joints and their range of motion on the [Hardware](/Introduction/hardware.md) page.

