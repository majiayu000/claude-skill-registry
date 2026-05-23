---
name: mobile-input
description: Implements mobile and touch input systems including virtual joysticks, touch buttons, gestures, and cross-platform input handling. Use when building games that need to work well on mobile devices.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Mobile Input Systems

When implementing touch controls, follow these patterns for responsive mobile gameplay.

## Platform Detection

```lua
local UserInputService = game:GetService("UserInputService")
local GuiService = game:GetService("GuiService")

local function getPlatform()
    if UserInputService.TouchEnabled then
        if UserInputService.KeyboardEnabled then
            return "tablet"  -- Has both touch and keyboard (Surface, iPad with keyboard)
        else
            return "mobile"  -- Touch only (phone, tablet)
        end
    elseif UserInputService.GamepadEnabled then
        return "console"
    else
        return "desktop"
    end
end

local function isMobile()
    return UserInputService.TouchEnabled and not UserInputService.KeyboardEnabled
end

local function isTouch()
    return UserInputService.TouchEnabled
end

-- Detect phone vs tablet by screen size
local function isPhone()
    local viewport = workspace.CurrentCamera.ViewportSize
    return viewport.X < 800 or viewport.Y < 500
end
```

## Virtual Joystick

### Basic Joystick

```lua
local VirtualJoystick = {}
VirtualJoystick.__index = VirtualJoystick

function VirtualJoystick.new(config)
    local self = setmetatable({}, VirtualJoystick)

    self.size = config.size or 150
    self.deadzone = config.deadzone or 0.1
    self.position = config.position or UDim2.new(0.15, 0, 0.75, 0)

    -- State
    self.active = false
    self.direction = Vector2.new(0, 0)
    self.inputObject = nil

    self:createUI()
    self:setupInput()

    return self
end

function VirtualJoystick:createUI()
    -- Outer ring (background)
    self.outerRing = Instance.new("ImageLabel")
    self.outerRing.Name = "JoystickOuter"
    self.outerRing.Size = UDim2.new(0, self.size, 0, self.size)
    self.outerRing.Position = self.position
    self.outerRing.AnchorPoint = Vector2.new(0.5, 0.5)
    self.outerRing.BackgroundTransparency = 1
    self.outerRing.Image = "rbxassetid://5765786884"  -- Circular outline
    self.outerRing.ImageTransparency = 0.3

    -- Inner stick (thumb)
    self.innerStick = Instance.new("ImageLabel")
    self.innerStick.Name = "JoystickInner"
    self.innerStick.Size = UDim2.new(0, self.size * 0.4, 0, self.size * 0.4)
    self.innerStick.Position = UDim2.new(0.5, 0, 0.5, 0)
    self.innerStick.AnchorPoint = Vector2.new(0.5, 0.5)
    self.innerStick.BackgroundTransparency = 1
    self.innerStick.Image = "rbxassetid://5765786884"  -- Filled circle
    self.innerStick.ImageTransparency = 0.1
    self.innerStick.Parent = self.outerRing

    -- Parent to ScreenGui
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "JoystickGui"
    screenGui.ResetOnSpawn = false
    screenGui.DisplayOrder = 100
    screenGui.Parent = game.Players.LocalPlayer:WaitForChild("PlayerGui")

    self.outerRing.Parent = screenGui
    self.gui = screenGui
end

function VirtualJoystick:setupInput()
    self.outerRing.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            self.active = true
            self.inputObject = input
            self:updateStick(input.Position)
        end
    end)

    self.outerRing.InputChanged:Connect(function(input)
        if self.active and input == self.inputObject then
            self:updateStick(input.Position)
        end
    end)

    self.outerRing.InputEnded:Connect(function(input)
        if input == self.inputObject then
            self:release()
        end
    end)
end

function VirtualJoystick:updateStick(touchPosition)
    local center = self.outerRing.AbsolutePosition +
        Vector2.new(self.outerRing.AbsoluteSize.X / 2, self.outerRing.AbsoluteSize.Y / 2)

    local offset = Vector2.new(touchPosition.X, touchPosition.Y) - center
    local maxDistance = self.size / 2

    -- Clamp to circle
    if offset.Magnitude > maxDistance then
        offset = offset.Unit * maxDistance
    end

    -- Update visual
    self.innerStick.Position = UDim2.new(
        0.5, offset.X,
        0.5, offset.Y
    )

    -- Calculate normalized direction
    self.direction = offset / maxDistance

    -- Apply deadzone
    if self.direction.Magnitude < self.deadzone then
        self.direction = Vector2.new(0, 0)
    end
end

function VirtualJoystick:release()
    self.active = false
    self.inputObject = nil
    self.direction = Vector2.new(0, 0)

    -- Reset visual
    self.innerStick.Position = UDim2.new(0.5, 0, 0.5, 0)
end

function VirtualJoystick:getDirection()
    return self.direction
end

function VirtualJoystick:getMagnitude()
    return self.direction.Magnitude
end

function VirtualJoystick:destroy()
    self.gui:Destroy()
end
```

### Dynamic Position Joystick

```lua
-- Joystick appears where you touch
local DynamicJoystick = {}
DynamicJoystick.__index = DynamicJoystick
setmetatable(DynamicJoystick, {__index = VirtualJoystick})

function DynamicJoystick.new(config)
    local self = VirtualJoystick.new(config)
    setmetatable(self, DynamicJoystick)

    self.outerRing.Visible = false
    self:setupDynamicInput()

    return self
end

function DynamicJoystick:setupDynamicInput()
    -- Touch zone covers left half of screen
    local touchZone = Instance.new("Frame")
    touchZone.Size = UDim2.new(0.5, 0, 1, 0)
    touchZone.Position = UDim2.new(0, 0, 0, 0)
    touchZone.BackgroundTransparency = 1
    touchZone.Parent = self.gui

    touchZone.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            -- Move joystick to touch position
            self.outerRing.Position = UDim2.new(0, input.Position.X, 0, input.Position.Y)
            self.outerRing.Visible = true

            self.active = true
            self.inputObject = input
            self.startPosition = Vector2.new(input.Position.X, input.Position.Y)
        end
    end)

    UserInputService.TouchMoved:Connect(function(input)
        if self.active and input == self.inputObject then
            self:updateStick(input.Position)
        end
    end)

    UserInputService.TouchEnded:Connect(function(input)
        if input == self.inputObject then
            self:release()
            self.outerRing.Visible = false
        end
    end)
end
```

## Touch Buttons

### Action Button

```lua
local function createActionButton(config)
    local button = Instance.new("ImageButton")
    button.Name = config.name or "ActionButton"
    button.Size = UDim2.new(0, config.size or 80, 0, config.size or 80)
    button.Position = config.position
    button.AnchorPoint = Vector2.new(0.5, 0.5)
    button.BackgroundTransparency = 1
    button.Image = config.image or "rbxassetid://5765786884"
    button.ImageTransparency = 0.3

    -- Label
    if config.label then
        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, 0, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = config.label
        label.TextColor3 = Color3.new(1, 1, 1)
        label.TextScaled = true
        label.Parent = button
    end

    -- Icon
    if config.icon then
        local icon = Instance.new("ImageLabel")
        icon.Size = UDim2.new(0.6, 0, 0.6, 0)
        icon.Position = UDim2.new(0.5, 0, 0.5, 0)
        icon.AnchorPoint = Vector2.new(0.5, 0.5)
        icon.BackgroundTransparency = 1
        icon.Image = config.icon
        icon.Parent = button
    end

    -- Press feedback
    button.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            button.ImageTransparency = 0.1
            button.Size = UDim2.new(0, (config.size or 80) * 0.9, 0, (config.size or 80) * 0.9)
        end
    end)

    button.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            button.ImageTransparency = 0.3
            button.Size = UDim2.new(0, config.size or 80, 0, config.size or 80)
        end
    end)

    return button
end

-- Common action buttons
local function createMobileControls(parent)
    -- Jump button
    local jumpButton = createActionButton({
        name = "JumpButton",
        position = UDim2.new(0.9, 0, 0.7, 0),
        size = 90,
        label = "JUMP"
    })
    jumpButton.Parent = parent

    jumpButton.MouseButton1Down:Connect(function()
        local humanoid = game.Players.LocalPlayer.Character
            and game.Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
        end
    end)

    -- Attack button
    local attackButton = createActionButton({
        name = "AttackButton",
        position = UDim2.new(0.75, 0, 0.85, 0),
        size = 70,
        label = "ATK"
    })
    attackButton.Parent = parent

    attackButton.MouseButton1Down:Connect(function()
        -- Fire attack event
        AttackRemote:FireServer()
    end)

    -- Ability buttons
    for i = 1, 3 do
        local abilityButton = createActionButton({
            name = "Ability" .. i,
            position = UDim2.new(0.6 + (i - 1) * 0.1, 0, 0.55, 0),
            size = 60,
            label = tostring(i)
        })
        abilityButton.Parent = parent

        abilityButton.MouseButton1Down:Connect(function()
            AbilityRemote:FireServer(i)
        end)
    end
end
```

### Holdable Button

```lua
local function createHoldButton(config)
    local button = createActionButton(config)

    local holding = false
    local holdStartTime = 0

    button.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            holding = true
            holdStartTime = os.clock()

            -- Hold loop
            task.spawn(function()
                while holding do
                    local holdTime = os.clock() - holdStartTime

                    if config.onHold then
                        config.onHold(holdTime)
                    end

                    task.wait()
                end
            end)
        end
    end)

    button.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            holding = false

            if config.onRelease then
                config.onRelease(os.clock() - holdStartTime)
            end
        end
    end)

    return button
end

-- Example: Charge attack
local chargeButton = createHoldButton({
    name = "ChargeAttack",
    position = UDim2.new(0.85, 0, 0.6, 0),
    onHold = function(holdTime)
        -- Update charge UI
        local charge = math.min(holdTime / 2, 1)  -- Max 2 seconds
        chargeBar.Size = UDim2.new(charge, 0, 1, 0)
    end,
    onRelease = function(holdTime)
        local charge = math.min(holdTime / 2, 1)
        ChargeAttackRemote:FireServer(charge)
    end
})
```

## Gesture Recognition

### Swipe Detection

```lua
local SwipeDetector = {}
SwipeDetector.minSwipeDistance = 50  -- pixels
SwipeDetector.maxSwipeTime = 0.3     -- seconds

local touchStart = {}

function SwipeDetector.init(callback)
    UserInputService.TouchStarted:Connect(function(input)
        touchStart[input] = {
            position = input.Position,
            time = os.clock()
        }
    end)

    UserInputService.TouchEnded:Connect(function(input)
        local startData = touchStart[input]
        if not startData then return end

        local endPosition = input.Position
        local deltaTime = os.clock() - startData.time

        if deltaTime > SwipeDetector.maxSwipeTime then
            touchStart[input] = nil
            return
        end

        local delta = Vector2.new(
            endPosition.X - startData.position.X,
            endPosition.Y - startData.position.Y
        )

        if delta.Magnitude < SwipeDetector.minSwipeDistance then
            touchStart[input] = nil
            return
        end

        -- Determine direction
        local direction
        if math.abs(delta.X) > math.abs(delta.Y) then
            direction = delta.X > 0 and "right" or "left"
        else
            direction = delta.Y > 0 and "down" or "up"
        end

        callback(direction, delta.Magnitude, deltaTime)

        touchStart[input] = nil
    end)
end

-- Usage
SwipeDetector.init(function(direction, distance, time)
    if direction == "up" then
        -- Jump or dodge up
        JumpRemote:FireServer()
    elseif direction == "down" then
        -- Slide or dodge down
        SlideRemote:FireServer()
    elseif direction == "left" then
        -- Dodge left
        DodgeRemote:FireServer("left")
    elseif direction == "right" then
        -- Dodge right
        DodgeRemote:FireServer("right")
    end
end)
```

### Pinch to Zoom

```lua
local PinchDetector = {}
local activeTouches = {}

function PinchDetector.init(onZoom)
    UserInputService.TouchStarted:Connect(function(input)
        activeTouches[input] = input.Position
    end)

    UserInputService.TouchMoved:Connect(function(input)
        if not activeTouches[input] then return end

        activeTouches[input] = input.Position

        -- Need exactly 2 touches for pinch
        local touches = {}
        for _, pos in pairs(activeTouches) do
            table.insert(touches, pos)
        end

        if #touches == 2 then
            local distance = (touches[1] - touches[2]).Magnitude

            if PinchDetector.lastDistance then
                local delta = distance - PinchDetector.lastDistance
                onZoom(delta / 100)  -- Normalize
            end

            PinchDetector.lastDistance = distance
        end
    end)

    UserInputService.TouchEnded:Connect(function(input)
        activeTouches[input] = nil
        PinchDetector.lastDistance = nil
    end)
end

-- Usage: Camera zoom
PinchDetector.init(function(zoomDelta)
    local camera = workspace.CurrentCamera
    -- Adjust camera distance
    CameraController.zoomLevel = math.clamp(
        CameraController.zoomLevel - zoomDelta * 5,
        5, 50
    )
end)
```

### Tap vs Long Press

```lua
local TapDetector = {}
TapDetector.longPressTime = 0.5  -- seconds
TapDetector.tapMaxMove = 20      -- pixels

function TapDetector.create(element, callbacks)
    local touchData = {}

    element.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            touchData = {
                startPosition = input.Position,
                startTime = os.clock(),
                moved = false
            }

            -- Long press timer
            task.delay(TapDetector.longPressTime, function()
                if touchData.startTime and not touchData.moved then
                    if callbacks.onLongPress then
                        callbacks.onLongPress()
                    end
                    touchData.handled = true
                end
            end)
        end
    end)

    element.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch and touchData.startPosition then
            local moved = (input.Position - touchData.startPosition).Magnitude
            if moved > TapDetector.tapMaxMove then
                touchData.moved = true
            end
        end
    end)

    element.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.Touch then
            if not touchData.handled and not touchData.moved then
                local duration = os.clock() - touchData.startTime

                if duration < TapDetector.longPressTime then
                    if callbacks.onTap then
                        callbacks.onTap()
                    end
                end
            end

            touchData = {}
        end
    end)
end

-- Usage
TapDetector.create(itemButton, {
    onTap = function()
        -- Quick select
        selectItem(itemId)
    end,
    onLongPress = function()
        -- Show item details
        showItemDetails(itemId)
    end
})
```

## Cross-Platform Input

### Unified Input System

```lua
local InputController = {}
InputController.moveDirection = Vector2.new(0, 0)
InputController.lookDirection = Vector2.new(0, 0)
InputController.actions = {}

-- Mobile joystick
local moveJoystick
local lookJoystick

function InputController.init()
    local platform = getPlatform()

    if platform == "mobile" or platform == "tablet" then
        -- Create touch controls
        moveJoystick = VirtualJoystick.new({
            position = UDim2.new(0.15, 0, 0.75, 0)
        })

        lookJoystick = VirtualJoystick.new({
            position = UDim2.new(0.85, 0, 0.75, 0)
        })

        createMobileControls(moveJoystick.gui)
    end

    -- Keyboard/Gamepad (always active as fallback)
    setupKeyboardInput()
    setupGamepadInput()
end

function InputController.update()
    -- Reset
    InputController.moveDirection = Vector2.new(0, 0)
    InputController.lookDirection = Vector2.new(0, 0)

    -- Mobile joysticks
    if moveJoystick and moveJoystick.active then
        InputController.moveDirection = moveJoystick:getDirection()
    end

    if lookJoystick and lookJoystick.active then
        InputController.lookDirection = lookJoystick:getDirection()
    end

    -- Keyboard WASD (if not using joystick)
    if InputController.moveDirection.Magnitude < 0.1 then
        local keyMove = Vector2.new(0, 0)

        if UserInputService:IsKeyDown(Enum.KeyCode.W) then
            keyMove = keyMove + Vector2.new(0, -1)
        end
        if UserInputService:IsKeyDown(Enum.KeyCode.S) then
            keyMove = keyMove + Vector2.new(0, 1)
        end
        if UserInputService:IsKeyDown(Enum.KeyCode.A) then
            keyMove = keyMove + Vector2.new(-1, 0)
        end
        if UserInputService:IsKeyDown(Enum.KeyCode.D) then
            keyMove = keyMove + Vector2.new(1, 0)
        end

        if keyMove.Magnitude > 0 then
            InputController.moveDirection = keyMove.Unit
        end
    end

    -- Gamepad
    local gamepadMove = UserInputService:GetGamepadState(Enum.UserInputType.Gamepad1)
    for _, input in ipairs(gamepadMove) do
        if input.KeyCode == Enum.KeyCode.Thumbstick1 then
            if input.Position.Magnitude > 0.1 then
                InputController.moveDirection = Vector2.new(input.Position.X, -input.Position.Y)
            end
        elseif input.KeyCode == Enum.KeyCode.Thumbstick2 then
            if input.Position.Magnitude > 0.1 then
                InputController.lookDirection = Vector2.new(input.Position.X, -input.Position.Y)
            end
        end
    end
end

function setupKeyboardInput()
    UserInputService.InputBegan:Connect(function(input, processed)
        if processed then return end

        if input.KeyCode == Enum.KeyCode.Space then
            InputController.actions.jump = true
        elseif input.KeyCode == Enum.KeyCode.E then
            InputController.actions.interact = true
        elseif input.KeyCode == Enum.KeyCode.Q then
            InputController.actions.ability1 = true
        end
    end)

    UserInputService.InputEnded:Connect(function(input)
        if input.KeyCode == Enum.KeyCode.Space then
            InputController.actions.jump = false
        elseif input.KeyCode == Enum.KeyCode.E then
            InputController.actions.interact = false
        end
    end)
end

function setupGamepadInput()
    UserInputService.InputBegan:Connect(function(input, processed)
        if processed then return end

        if input.KeyCode == Enum.KeyCode.ButtonA then
            InputController.actions.jump = true
        elseif input.KeyCode == Enum.KeyCode.ButtonX then
            InputController.actions.interact = true
        elseif input.KeyCode == Enum.KeyCode.ButtonB then
            InputController.actions.attack = true
        end
    end)
end

-- Usage in character controller
RunService.RenderStepped:Connect(function()
    InputController.update()

    local humanoid = LocalPlayer.Character
        and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")

    if humanoid then
        -- Convert 2D input to 3D movement
        local camera = workspace.CurrentCamera
        local cameraForward = camera.CFrame.LookVector * Vector3.new(1, 0, 1)
        local cameraRight = camera.CFrame.RightVector * Vector3.new(1, 0, 1)

        local moveDir = InputController.moveDirection
        local worldDirection = (cameraForward.Unit * -moveDir.Y + cameraRight.Unit * moveDir.X)

        if worldDirection.Magnitude > 0 then
            humanoid:Move(worldDirection.Unit)
        else
            humanoid:Move(Vector3.new(0, 0, 0))
        end

        if InputController.actions.jump then
            humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
        end
    end
end)
```

## Mobile UI Scaling

```lua
local function createResponsiveUI()
    local screenGui = Instance.new("ScreenGui")
    screenGui.ResetOnSpawn = false

    -- Different layouts based on platform
    local platform = getPlatform()
    local isPortrait = workspace.CurrentCamera.ViewportSize.Y >
                       workspace.CurrentCamera.ViewportSize.X

    -- Control container
    local controls = Instance.new("Frame")
    controls.Size = UDim2.new(1, 0, 1, 0)
    controls.BackgroundTransparency = 1
    controls.Parent = screenGui

    if platform == "mobile" then
        if isPhone() then
            -- Smaller controls for phone
            controls:SetAttribute("ControlScale", 0.7)
        else
            -- Tablet gets larger controls
            controls:SetAttribute("ControlScale", 1)
        end

        -- Portrait vs landscape
        if isPortrait then
            -- Stack controls vertically
            controls:SetAttribute("Layout", "portrait")
        else
            -- Controls on sides
            controls:SetAttribute("Layout", "landscape")
        end
    end

    -- Update on rotation
    workspace.CurrentCamera:GetPropertyChangedSignal("ViewportSize"):Connect(function()
        local newPortrait = workspace.CurrentCamera.ViewportSize.Y >
                           workspace.CurrentCamera.ViewportSize.X

        if newPortrait ~= isPortrait then
            isPortrait = newPortrait
            updateLayout(controls, isPortrait)
        end
    end)

    return screenGui
end

local function updateLayout(controls, isPortrait)
    -- Reposition elements based on orientation
    local joystickLeft = controls:FindFirstChild("JoystickLeft")
    local joystickRight = controls:FindFirstChild("JoystickRight")
    local buttons = controls:FindFirstChild("ActionButtons")

    if isPortrait then
        -- Portrait: controls at bottom
        if joystickLeft then
            joystickLeft.Position = UDim2.new(0.25, 0, 0.85, 0)
        end
        if joystickRight then
            joystickRight.Position = UDim2.new(0.75, 0, 0.85, 0)
        end
        if buttons then
            buttons.Position = UDim2.new(0.5, 0, 0.7, 0)
        end
    else
        -- Landscape: controls on sides
        if joystickLeft then
            joystickLeft.Position = UDim2.new(0.12, 0, 0.75, 0)
        end
        if joystickRight then
            joystickRight.Position = UDim2.new(0.88, 0, 0.75, 0)
        end
        if buttons then
            buttons.Position = UDim2.new(0.75, 0, 0.5, 0)
        end
    end
end
```

## Safe Areas (Notch/Home Indicator)

```lua
local GuiService = game:GetService("GuiService")

local function getSafeAreaInsets()
    local inset = GuiService:GetGuiInset()
    return {
        top = inset.Y,
        bottom = 0,  -- Check specific device
        left = 0,
        right = 0
    }
end

local function applySafeArea(element)
    local insets = getSafeAreaInsets()

    -- Adjust position to avoid notch/home indicator
    local currentPos = element.Position

    element.Position = UDim2.new(
        currentPos.X.Scale,
        currentPos.X.Offset + insets.left,
        currentPos.Y.Scale,
        currentPos.Y.Offset + insets.top
    )
end

-- Or use ScreenGui.SafeAreaCompatibility
local screenGui = Instance.new("ScreenGui")
screenGui.SafeAreaCompatibility = Enum.SafeAreaCompatibility.FullscreenExtension
-- Enum.SafeAreaCompatibility.None - Ignore safe areas
-- Enum.SafeAreaCompatibility.FullscreenExtension - Extend behind notch
```

## Complete Mobile Setup

```lua
-- MobileController.lua (LocalScript in StarterPlayerScripts)
local MobileController = {}

function MobileController.init()
    -- Only setup on touch devices
    if not UserInputService.TouchEnabled then
        return
    end

    -- Create main GUI
    local gui = Instance.new("ScreenGui")
    gui.Name = "MobileControls"
    gui.ResetOnSpawn = false
    gui.DisplayOrder = 10
    gui.Parent = game.Players.LocalPlayer:WaitForChild("PlayerGui")

    -- Create joysticks
    MobileController.moveJoystick = DynamicJoystick.new({
        size = isPhone() and 100 or 150,
        position = UDim2.new(0.15, 0, 0.75, 0)
    })
    MobileController.moveJoystick.gui.Parent = gui

    -- Create action buttons
    local actionContainer = Instance.new("Frame")
    actionContainer.Size = UDim2.new(0.3, 0, 0.4, 0)
    actionContainer.Position = UDim2.new(0.95, 0, 0.8, 0)
    actionContainer.AnchorPoint = Vector2.new(1, 1)
    actionContainer.BackgroundTransparency = 1
    actionContainer.Parent = gui

    -- Jump button (bottom right)
    local jumpBtn = createActionButton({
        name = "Jump",
        size = isPhone() and 70 or 90,
        position = UDim2.new(0.5, 0, 0.7, 0),
        icon = "rbxassetid://123456"  -- Jump icon
    })
    jumpBtn.Parent = actionContainer

    -- Attack button (right of jump)
    local attackBtn = createActionButton({
        name = "Attack",
        size = isPhone() and 60 or 80,
        position = UDim2.new(0.15, 0, 0.4, 0),
        icon = "rbxassetid://123457"  -- Attack icon
    })
    attackBtn.Parent = actionContainer

    -- Connect buttons to actions
    jumpBtn.MouseButton1Down:Connect(function()
        local humanoid = game.Players.LocalPlayer.Character
            and game.Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
        end
    end)

    attackBtn.MouseButton1Down:Connect(function()
        AttackRemote:FireServer()
    end)

    -- Swipe gestures for dodge
    SwipeDetector.init(function(direction)
        DodgeRemote:FireServer(direction)
    end)

    -- Update loop
    RunService.RenderStepped:Connect(function()
        MobileController.update()
    end)
end

function MobileController.update()
    local moveDir = MobileController.moveJoystick:getDirection()

    if moveDir.Magnitude > 0.1 then
        local camera = workspace.CurrentCamera
        local cameraForward = camera.CFrame.LookVector * Vector3.new(1, 0, 1)
        local cameraRight = camera.CFrame.RightVector * Vector3.new(1, 0, 1)

        local worldDir = (cameraForward.Unit * -moveDir.Y + cameraRight.Unit * moveDir.X)

        local humanoid = game.Players.LocalPlayer.Character
            and game.Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")

        if humanoid then
            humanoid:Move(worldDir.Unit)
        end
    end
end

return MobileController
```
