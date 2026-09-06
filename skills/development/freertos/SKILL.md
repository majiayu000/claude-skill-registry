---
name: freertos
description: 'Use when creating FreeRTOS tasks, queues, semaphores, or mutexes, catching stack overflow, writing FreeRTOSConfig.h, or debugging tasks over OpenOCD and GDB. Not for probe setup: use openocd-jtag.'
---

# FreeRTOS

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A FreeRTOS application needs tasks, inter-task communication, stack overflow detection, a `FreeRTOSConfig.h`, or thread-aware debugging through OpenOCD and GDB. |
| Authority | Reversible local: writes only the application sources and `FreeRTOSConfig.h` in the project directory the user names; rollback is reverting those files in version control. No remote mutation. |
| Side effect | New or edited C sources and configuration in the project. A debug session halts and resumes the target. |
| Done | The scheduler starts, every task runs at its intended priority, shared resources are guarded by a mutex, `configCHECK_FOR_STACK_OVERFLOW` and `configASSERT` are on with hooks that stop the core, and `info threads` in GDB lists the tasks. |

## Inputs

- FreeRTOS kernel version (`tskKERNEL_VERSION_NUMBER` in `task.h`; V11.3.1 is the current release on 2026-09-05).
- Port: CPU core and compiler (for example GCC on Cortex-M4, which sets `configPRIO_BITS` and the interrupt priority rules).
- The tasks, their periods, and which data flows between them.
- Heap budget and the RAM regions available for it.
- Debug transport, if any (OpenOCD config, see `openocd-jtag`).

## Procedure

1. Create tasks. `usStackDepth` is in words, not bytes. Higher numbers are more urgent; `tskIDLE_PRIORITY` is 0 and the highest usable priority is `configMAX_PRIORITIES - 1`. A task function never returns. Done when: `vTaskStartScheduler()` is called after every task and queue is created, and no task function has a return path.

   ```c
   #include "FreeRTOS.h"
   #include "task.h"

   void vSensorTask(void *pvParameters) {
       for (;;) {
           read_sensor();
           vTaskDelay(pdMS_TO_TICKS(500));
       }
   }

   int main(void) {
       TaskHandle_t xHandle = NULL;
       xTaskCreate(vSensorTask, "sensor",
                   configMINIMAL_STACK_SIZE + 128,   /* words */
                   NULL, tskIDLE_PRIORITY + 2, &xHandle);
       vTaskStartScheduler();                        /* returns only if the heap is too small */
       for (;;);
   }
   ```

   Give the task that services an interrupt the highest priority among application tasks so the ISR can stay short.

2. Pass data through queues. `xQueueSend` copies the item; the third argument is the block time when the queue is full. From an ISR use `xQueueSendFromISR` with `pxHigherPriorityTaskWoken` and call `portYIELD_FROM_ISR` on the way out. Done when: every producer and consumer pair shares one queue created before the scheduler starts.

   ```c
   #include "queue.h"

   typedef struct { uint32_t sensor_id; float value; } SensorReading_t;
   QueueHandle_t xSensorQueue;

   void vProducerTask(void *p) {
       SensorReading_t r = { .sensor_id = 1 };
       for (;;) {
           r.value = read_adc();
           xQueueSend(xSensorQueue, &r, pdMS_TO_TICKS(10));
           vTaskDelay(pdMS_TO_TICKS(100));
       }
   }

   void vConsumerTask(void *p) {
       SensorReading_t r;
       for (;;) {
           if (xQueueReceive(xSensorQueue, &r, portMAX_DELAY) == pdTRUE) {
               process(r.value);
           }
       }
   }

   /* before vTaskStartScheduler() */
   xSensorQueue = xQueueCreate(10, sizeof(SensorReading_t));
   ```

3. Signal with a binary semaphore and guard with a mutex. A binary semaphore carries an event from an ISR to a task. A mutex protects a shared resource and provides priority inheritance, which a semaphore does not; a mutex is never taken or given from an ISR. Done when: every shared resource is behind a mutex and every ISR-to-task signal uses a semaphore, a queue, or a task notification.

   ```c
   #include "semphr.h"

   SemaphoreHandle_t xSem = xSemaphoreCreateBinary();

   void UART_ISR(void) {
       BaseType_t xWoken = pdFALSE;
       xSemaphoreGiveFromISR(xSem, &xWoken);
       portYIELD_FROM_ISR(xWoken);
   }

   void vUartTask(void *p) {
       for (;;) {
           xSemaphoreTake(xSem, portMAX_DELAY);
           drain_uart();
       }
   }

   SemaphoreHandle_t xMutex = xSemaphoreCreateMutex();

   void update_shared(void) {
       if (xSemaphoreTake(xMutex, pdMS_TO_TICKS(100)) == pdTRUE) {
           shared_resource++;
           xSemaphoreGive(xMutex);
       }
   }
   ```

   `xSemaphoreCreateRecursiveMutex` with `xSemaphoreTakeRecursive` and `xSemaphoreGiveRecursive` lets one task take the same mutex more than once.

4. Turn on stack overflow detection and the hooks. Method 2 checks a fill pattern at the top of the stack on every context switch and catches more overflows than method 1, which checks only the stack pointer. Done when: both hooks exist and stop the core, and `uxTaskGetStackHighWaterMark` has been read for every task under its worst-case load.

   ```c
   /* FreeRTOSConfig.h */
   #define configCHECK_FOR_STACK_OVERFLOW  2
   #define configUSE_MALLOC_FAILED_HOOK    1

   void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
       (void)xTask; (void)pcTaskName;
       taskDISABLE_INTERRUPTS();
       for (;;);
   }

   void vApplicationMallocFailedHook(void) {
       taskDISABLE_INTERRUPTS();
       for (;;);
   }

   UBaseType_t headroom = uxTaskGetStackHighWaterMark(xHandle);  /* minimum ever free, in words */
   ```

   The right stack size comes from the measured high-water mark under the task's worst-case call depth plus the interrupt frame the port pushes, not from a fixed number.

5. Write `FreeRTOSConfig.h`. Start from the template the kernel ships in `examples/template_configuration/FreeRTOSConfig.h` (V11.0.0 and later) and set the values for your MCU. `references/freertos-config.md` explains each group. Done when: the file compiles, `configASSERT` stops the core, and the Cortex-M interrupt priority values match the NVIC priority bits of the part.

   ```c
   #define configCPU_CLOCK_HZ              (SystemCoreClock)
   #define configTICK_RATE_HZ              1000
   #define configMAX_PRIORITIES            8
   #define configMINIMAL_STACK_SIZE        128           /* words */
   #define configTOTAL_HEAP_SIZE           (16 * 1024)   /* bytes */
   #define configMAX_TASK_NAME_LEN         16

   #define configUSE_TRACE_FACILITY        1
   #define configUSE_STATS_FORMATTING_FUNCTIONS 1
   #define configCHECK_FOR_STACK_OVERFLOW  2
   #define configUSE_MALLOC_FAILED_HOOK    1
   #define configASSERT(x) if ((x) == 0) { taskDISABLE_INTERRUPTS(); for (;;); }

   #define configUSE_MUTEXES               1
   #define configUSE_RECURSIVE_MUTEXES     1
   #define configUSE_COUNTING_SEMAPHORES   1
   #define configUSE_TIMERS                1
   #define configTIMER_TASK_STACK_DEPTH    (configMINIMAL_STACK_SIZE * 2)
   ```

6. Debug with thread awareness. OpenOCD's RTOS support reads the task list from kernel symbols; enable it per target and keep `configUSE_TRACE_FACILITY` at 1 so the symbols exist. Done when: `info threads` in GDB lists every task by name.

   ```tcl
   # openocd.cfg, after the target config
   $_TARGETNAME configure -rtos auto     # or: -rtos FreeRTOS
   ```

   ```
   (gdb) info threads      # one row per task
   (gdb) thread 3
   (gdb) bt                # that task's stack
   (gdb) call vTaskList(buf)
   (gdb) printf "%s\n", buf
   ```

   The OpenOCD user guide notes that FreeRTOS may need an extra OpenOCD-specific object linked into the firmware for symbol access; follow the "RTOS Support" section for the kernel version in use.

7. Use the newer kernel APIs where they fit. Indexed task notifications (`xTaskNotifyIndexed`, `xTaskNotifyWaitIndexed`) and stream buffers (`xStreamBufferSend`, `xStreamBufferSetTriggerLevel`) are in V10.4 and later; V11.0.0 added symmetric multiprocessing to the mainline. Check `tskKERNEL_VERSION_NUMBER` before relying on any of them. Done when: no API call is newer than the kernel in the tree.

   ```c
   xTaskNotifyIndexed(xHandle, 0, ulValue, eSetValueWithOverwrite);
   xTaskNotifyWaitIndexed(0, 0, ULONG_MAX, &ulNotified, portMAX_DELAY);

   xStreamBufferSend(xStream, data, len, 0);
   xStreamBufferSetTriggerLevel(xStream, 1);   /* wake the receiver on one byte */
   ```

8. Restrict a task with the MPU when the port supports it. `xTaskCreateRestricted` takes a `TaskParameters_t` with up to `portNUM_CONFIGURABLE_REGIONS` regions; a zero-length region ends the list. On ARMv8-M with TrustZone, a task that calls secure functions allocates a secure context with `portALLOCATE_SECURE_CONTEXT(size)` after `SecureContext_Init()` on the secure side, with `configENABLE_TRUSTZONE` set. Done when: the restricted task runs and a deliberate write outside its regions raises the MemManage fault.

   ```c
   static const TaskParameters_t xRestricted = {
       .pvTaskCode = vRestrictedTask,
       .pcName = "restricted",
       .usStackDepth = configMINIMAL_STACK_SIZE,
       .pvParameters = NULL,
       .uxPriority = tskIDLE_PRIORITY + 1,
       .puxStackBuffer = stackBuffer,
       .xRegions = {
           { (void *)0x20000000, 0x10000, tskMPU_REGION_READ_ONLY | tskMPU_REGION_EXECUTE_NEVER },
           { NULL, 0, 0 },
       },
   };
   xTaskCreateRestricted(&xRestricted, &xHandle);
   ```

9. For TCP, use FreeRTOS+TCP after `FreeRTOS_IPInit`. Buffer counts and protocol switches live in `FreeRTOSIPConfig.h` (`ipconfigUSE_TCP`, `ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS`). Done when: `FreeRTOS_socket`, `FreeRTOS_connect`, and `FreeRTOS_send` move bytes to a peer.

   ```c
   #include "FreeRTOS_IP.h"
   #include "FreeRTOS_Sockets.h"

   Socket_t s = FreeRTOS_socket(FREERTOS_AF_INET, FREERTOS_SOCK_STREAM, FREERTOS_IPPROTO_TCP);
   FreeRTOS_connect(s, &xAddress, sizeof(xAddress));
   FreeRTOS_send(s, buffer, len, 0);
   ```

## Failure and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `vTaskStartScheduler()` returns | Heap too small for the idle or timer task | Raise `configTOTAL_HEAP_SIZE`; check `xPortGetFreeHeapSize()` before starting. |
| Random corruption or HardFault in one task | Stack overflow | Set `configCHECK_FOR_STACK_OVERFLOW 2`; read the high-water mark; grow that task's stack. |
| `configASSERT` fires inside a `FromISR` call | ISR priority numerically below `configMAX_SYSCALL_INTERRUPT_PRIORITY` | Set the NVIC priority so it is equal to or greater than the limit (see the reference). |
| Deadlock between two tasks | Two mutexes taken in opposite order | Fix the lock order, or merge into one mutex. |
| `info threads` shows one thread | RTOS support not enabled in OpenOCD, or trace facility off | Add `configure -rtos auto`; set `configUSE_TRACE_FACILITY 1`. |
| Task created but never runs | Priority below a task that never blocks | Make every task block (`vTaskDelay`, queue receive, or notification wait). |

## Output

A FreeRTOS application in the named directory with tasks, queues, and mutexes as designed, a `FreeRTOSConfig.h` with overflow detection and asserts on, and, when a probe is present, a GDB session that lists tasks with `info threads`.
