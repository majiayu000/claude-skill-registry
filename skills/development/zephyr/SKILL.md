---
name: zephyr
description: 'Use when building a Zephyr app with west, picking a board target, editing prj.conf or a devicetree overlay, adding logging, running on native_sim, or using west debug. Not for FreeRTOS: use freertos.'
---

# Zephyr RTOS

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A Zephyr application must be created, built, configured through Kconfig or devicetree, given logging, run on the host with `native_sim`, or debugged on hardware. |
| Authority | Reversible local: writes only the application directory the user names (`CMakeLists.txt`, `prj.conf`, overlays, `src/`) and, when asked, a `west.yml` manifest; rollback is reverting those files in version control. No remote mutation. |
| Side effect | New or edited application files. `west update` clones modules into the workspace. `west flash` rewrites the board's flash. |
| Done | `west build -b <board> <app>` produces `build/zephyr/zephyr.elf`, the same application builds for `native_sim` and prints its log lines when run, and on hardware `west flash` followed by a serial monitor shows the same lines. |

## Inputs

- Board target in `board/soc` form (`west boards` lists them).
- Zephyr version to pin (v4.4.2 is the current release on 2026-09-05; v3.7 is the older long-term branch) and the matching Zephyr SDK (1.0.1 on the same date).
- The peripherals the application needs, so the overlay and Kconfig can be scoped.
- A debug adapter, if hardware debugging is wanted (see `openocd-jtag`).

## Procedure

1. Set up the workspace once. `west init` clones the manifest repository, `west update` fetches every module it lists, `west zephyr-export` registers the CMake package, `west packages pip --install` installs the Python requirements, and `west sdk install` fetches the toolchains. Done when: `west build -b nrf52840dk/nrf52840 zephyr/samples/hello_world` succeeds from the workspace root.

   ```bash
   pip install west
   west init ~/zephyrproject
   west update
   west zephyr-export
   west packages pip --install
   west sdk install
   west build -b nrf52840dk/nrf52840 zephyr/samples/hello_world
   west flash
   ```

   Board names: `nrf52840dk/nrf52840`, `nucleo_f446re`, `rpi_pico/rp2040`, `esp32_devkitc_wroom/esp32/procpu`, `qemu_cortex_m3`, `native_sim`. Read the serial console with any terminal program at the board's baud, for example `screen /dev/ttyACM0 115200`.

2. Lay out the application. `find_package(Zephyr)` pulls in the build system; `app` is the library target every Zephyr application adds sources to. Done when: the directory below builds for the chosen board.

   ```
   my_app/
   ├── CMakeLists.txt
   ├── prj.conf
   ├── app.overlay
   └── src/main.c
   ```

   ```cmake
   cmake_minimum_required(VERSION 3.28.0)
   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
   project(my_app)
   target_sources(app PRIVATE src/main.c)
   ```

3. Configure features in `prj.conf`. Each line is `CONFIG_<symbol>=<value>`; the build merges it over the board defaults. `west build -t menuconfig` and `-t guiconfig` browse the tree and show what each symbol depends on. Done when: `build/zephyr/.config` contains every symbol the application relies on.

   ```
   CONFIG_GPIO=y
   CONFIG_UART_CONSOLE=y
   CONFIG_LOG=y
   CONFIG_LOG_DEFAULT_LEVEL=3
   CONFIG_PRINTK=y
   CONFIG_HEAP_MEM_POOL_SIZE=4096
   CONFIG_MAIN_STACK_SIZE=2048
   ```

   `LOG_DEFAULT_LEVEL` values: 0 off, 1 error, 2 warning, 3 info, 4 debug.

4. Describe hardware in a devicetree overlay. The board's `.dts` is fixed; `app.overlay` adds nodes and changes properties. C code reaches nodes through the `DT_*` macros and the `*_dt_spec` helpers. Done when: `GPIO_DT_SPEC_GET` on the alias compiles and toggles the pin.

   ```dts
   / {
       leds {
           compatible = "gpio-leds";
           my_led: led_0 {
               gpios = <&gpio0 13 GPIO_ACTIVE_LOW>;
           };
       };
       aliases { led0 = &my_led; };
   };

   &uart0 { current-speed = <115200>; };
   &spi1 { status = "disabled"; };
   ```

   ```c
   #include <zephyr/devicetree.h>
   #include <zephyr/drivers/gpio.h>

   static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);

   gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
   gpio_pin_toggle_dt(&led);
   ```

5. Log through the logging subsystem. `LOG_MODULE_REGISTER` names the module and sets its compile-time level; the backend is a Kconfig choice. Done when: the log lines appear on the chosen backend with the module name prefix.

   ```c
   #include <zephyr/logging/log.h>
   LOG_MODULE_REGISTER(my_module, LOG_LEVEL_DBG);

   LOG_INF("sensor %d", value);
   LOG_WRN("battery %d%%", battery_pct);
   LOG_ERR("spi %d", ret);
   LOG_HEXDUMP_DBG(buf, len, "raw");
   ```

   ```
   CONFIG_LOG=y
   CONFIG_LOG_BACKEND_UART=y
   CONFIG_LOG_BACKEND_RTT=y
   CONFIG_LOG_PROCESS_THREAD_STACK_SIZE=1024
   ```

6. Run on the host with `native_sim`. Zephyr links into a Linux executable; the UART appears on a pseudo-terminal whose path the program prints at start. Done when: `./build/zephyr/zephyr.exe` prints the application's log lines and exits under `gdb` with a readable backtrace.

   ```bash
   west build -b native_sim my_app
   ./build/zephyr/zephyr.exe
   ./build/zephyr/zephyr.exe --help     # native_sim command-line options
   gdb --args ./build/zephyr/zephyr.exe
   ```

   Use `native_sim` for unit tests and CI; validate timing, DMA, and peripheral behavior on hardware.

7. Debug on hardware. `west debug` starts the board's runner (OpenOCD, J-Link, or pyOCD) and GDB together; `west attach` connects without flashing. For thread-aware `info threads` through OpenOCD, set `CONFIG_DEBUG_THREAD_INFO=y` so the kernel emits the symbols OpenOCD's RTOS support reads. Done when: `west debug` stops at `main` and `info threads` lists the kernel threads.

   ```bash
   west debug
   west attach
   ```

   `references/west-manifest.md` covers pinning Zephyr and adding a module in `west.yml`.

## Failure and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `west: unknown command "build"` | Not inside a west workspace | Run from the workspace, or `west init` first. |
| `Could not find a package configuration file provided by "Zephyr"` | `zephyr-export` not run, `ZEPHYR_BASE` unset | `west zephyr-export`; or export `ZEPHYR_BASE`. |
| Board name rejected | Old `board` form, or the SoC qualifier missing | Use the `board/soc` name from `west boards`. |
| `CONFIG_X` ignored | Dependency unmet | Open `west build -t menuconfig`, find the symbol, satisfy its `depends on`. |
| Devicetree node error at build | Wrong label or missing `compatible` | Check the board `.dts` in `build/zephyr/zephyr.dts` for the real labels. |
| `info threads` shows one thread | `CONFIG_DEBUG_THREAD_INFO` off, or RTOS support off in OpenOCD | Set it to `y`; add `configure -rtos auto` to the target. |

## Output

An application directory that builds for the named board and for `native_sim`, with `prj.conf`, overlay, and sources as designed, plus the `west` command lines that build, flash, and debug it.
