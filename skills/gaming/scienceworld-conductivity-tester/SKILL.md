---
name: scienceworld-conductivity-tester
description: Determines if an object is electrically conductive by integrating it into a circuit and observing a light bulb. Triggered when classifying an object based on conductivity.
---
# Instructions

## Objective
Classify a target object as **electrically conductive** or **non-conductive** by using it to complete a simple circuit with a battery and a light bulb.

## Core Procedure
1.  **Locate & Acquire Object:** Teleport to the object's location and pick it up.
2.  **Focus on Object:** Use the `focus` action on the object to signal intent.
3.  **Setup in Workshop:** Teleport to the `workshop`. Place the object down.
4.  **Construct Test Circuit:** Assemble the circuit on the table in this exact sequence:
    a. Connect the **battery anode** to **orange wire terminal 1**.
    b. Connect the **battery cathode** to **yellow wire terminal 1**.
    c. Connect **orange wire terminal 2** to the **blue light bulb cathode**.
    d. Connect **green wire terminal 2** to the **blue light bulb anode**.
    e. Connect **yellow wire terminal 2** to **terminal 1** on the target object.
    f. Connect **green wire terminal 1** to **terminal 2** on the target object.
5.  **Observe & Classify:** Wait 2 steps (`wait1` twice). Then `look around`.
    - If the **blue light bulb is ON**, the object is **conductive**. Place it in the **blue box**.
    - If the **blue light bulb is OFF**, the object is **non-conductive**. Place it in the **orange box**.

## Key Notes
- The `workshop` contains all necessary components: battery, wires (orange, yellow, green), and light bulbs.
- The circuit is fragile; connect components in the order specified.
- The observation (`look around`) after waiting is critical for determining the bulb's state.
- This skill assumes the environment's action set and room structure as provided in the trajectory.
