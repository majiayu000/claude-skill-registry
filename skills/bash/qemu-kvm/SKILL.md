---
name: qemu-kvm
description: 'Use when running qemu-system-x86_64 with KVM, wiring virtio devices, passing a PCI device through with VFIO, driving QMP, using virsh or virt-install, or booting a kernel with -kernel and -append.'
---

# QEMU and KVM

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A Linux VM needs hardware acceleration, a custom kernel needs booting without bare metal, a GPU or NIC needs passing to a guest, or a guest needs snapshots or scripted control. |
| Authority | Reversible local. The write set is QEMU processes started for the session, disk images and snapshots in user-named files, QMP sockets, libvirt domain definitions, and a PCI device rebound to `vfio-pci`. Rollback is stopping the process, deleting the image or snapshot, undefining the domain, and rebinding the device to its original driver. Rebinding a device and using `/dev/kvm` need root or group membership. No remote mutation. |
| Side effect | A guest runs and may hold a passed-through device while the session lasts. |
| Done | The guest boots to the console with KVM active, or the kernel under test reaches the breakpoint or panic under study, and every started process and rebound device has its teardown recorded. |

## Inputs

- Goal (required): run an image, boot a kernel, pass through a device, or manage through libvirt.
- Image or kernel (required): a qcow2 or raw disk, or a `bzImage` with an initramfs or root filesystem.
- Host state (required to know): whether `/dev/kvm` exists and is accessible, and whether the IOMMU is on for passthrough.

## Procedure

1. Confirm acceleration. Done when: `/dev/kvm` exists and the current user can open it.

```bash
grep -c -E 'vmx|svm' /proc/cpuinfo    # non-zero means the CPU can virtualize
ls -l /dev/kvm                          # group kvm; add the user or run as root
```

2. Start a plain guest. Done when: the guest console appears on the terminal.

```bash
qemu-system-x86_64 \
  -accel kvm -cpu host -m 4096 -smp 4 \
  -drive file=ubuntu.img,format=qcow2,if=virtio \
  -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
  -display none -serial mon:stdio
```

`-accel kvm` is the current spelling of `-enable-kvm`; both work. `-cpu host` exposes the host CPU model to the guest. `-m` is memory in MiB, `-smp` the vCPU count.

3. Use virtio for every device the guest can drive. Emulated IDE or e1000 devices work but cost far more exits. Done when: disk and network are virtio.

```bash
-device virtio-blk-pci,drive=hd0 -drive if=none,id=hd0,file=disk.qcow2,format=qcow2
-netdev tap,id=net0,ifname=tap0,script=no,downscript=no -device virtio-net-pci,netdev=net0
-device virtio-balloon-pci
-device virtio-scsi-pci,id=scsi0 -device scsi-hd,drive=hd0,bus=scsi0.0
```

4. Pass a PCI device through with VFIO. The kernel command line needs `intel_iommu=on` or `amd_iommu=on`, and the device's whole IOMMU group must go to the guest. Done when: `-device vfio-pci` starts without a group error and the guest sees the device.

```bash
find /sys/kernel/iommu_groups/ -type l              # which devices share a group
echo 10de 1c03 | sudo tee /sys/bus/pci/drivers/vfio-pci/new_id
sudo virsh nodedev-detach pci_0000_01_00_0          # when libvirt manages the host
qemu-system-x86_64 -accel kvm -m 8192 -smp 8 -device vfio-pci,host=01:00.0 ...
```

Record the device's original driver so it can be rebound afterward.

5. Drive the guest over QMP. Done when: `query-status` answers on the socket.

```bash
qemu-system-x86_64 ... -qmp unix:/tmp/qmp.sock,server=on,wait=off
socat - UNIX-CONNECT:/tmp/qmp.sock
{"execute":"qmp_capabilities"}
{"execute":"query-status"}
{"execute":"system_powerdown"}
```

`server=on,wait=off` is the current form of the older `server,nowait`.

6. Manage guests with libvirt when they must outlive the shell. Done when: `virsh list --all` shows the domain in the expected state.

```bash
virsh define myvm.xml
virsh start myvm
virsh console myvm
virsh shutdown myvm            # ACPI request
virsh destroy myvm             # hard power off
virsh snapshot-create-as myvm snap1 "before upgrade"
virsh list --all
```

```bash
virt-install \
  --name ubuntu-vm --memory 4096 --vcpus 4 \
  --disk path=/var/lib/libvirt/images/ubuntu.qcow2,size=20 \
  --osinfo ubuntu22.04 \
  --network bridge=virbr0 \
  --graphics none --console pty,target.type=serial \
  --location http://archive.ubuntu.com/ubuntu/dists/jammy/main/installer-amd64/ \
  --extra-args 'console=ttyS0,115200n8'
```

`--memory` replaces `--ram`; `--osinfo` is the current name of `--os-variant`, and `virt-install` fails when it cannot detect or is not given one.

7. Boot a kernel under development directly. Done when: the kernel prints on the serial console and mounts its root.

```bash
qemu-system-x86_64 -accel kvm -m 512 \
  -kernel arch/x86/boot/bzImage \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0 nokaslr" \
  -serial stdio -display none -no-reboot
```

With a root filesystem on a virtio disk: `-drive file=rootfs.ext4,format=raw,if=virtio -append "console=ttyS0 root=/dev/vda rw"`. `-no-reboot` makes a panic exit QEMU instead of looping.

8. Attach GDB to the kernel. `-s` opens the gdb stub on TCP 1234; `-S` holds the CPU until the debugger continues. `nokaslr` keeps symbols at their link addresses. Done when: `break start_kernel` hits.

```bash
qemu-system-x86_64 -kernel bzImage -append "console=ttyS0 nokaslr" -s -S -serial stdio -display none
gdb vmlinux
(gdb) target remote :1234
(gdb) break start_kernel
(gdb) continue
```

9. Manage images. Done when: the image or snapshot exists and `qemu-img info` lists it.

```bash
qemu-img create -f qcow2 disk.qcow2 20G
qemu-img snapshot -c clean disk.qcow2      # internal snapshot named "clean"
qemu-img convert -O raw disk.qcow2 disk.raw
qemu-img info disk.qcow2
```

For the hardware under KVM, use `hypervisor-internals`. For kernel test boots, use `kernel-testing`; for kgdb sessions, use `kernel-debugging`. For a minimal guest OS, use `os-dev-scratch`. For DPDK on virtio, use `dpdk`.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| KVM unavailable warning | VT-x or AMD-V is off in firmware, or the `kvm_intel`/`kvm_amd` module is not loaded. Enable it and check `/dev/kvm` again; do not fall back to TCG silently. |
| Guest very slow | KVM is not active. Add `-accel kvm` and confirm `/dev/kvm` is readable. |
| VFIO group error | Another device in the same IOMMU group still has a host driver. Bind the whole group or pick a device in its own group. |
| No network in guest | Backend mismatch. User networking gives outbound only; tap or bridge gives a routable interface. |
| Kernel panics at boot | Wrong `root=` or the initramfs lacks the virtio drivers. Fix the command line or add the modules. |
| QMP connection refused | QEMU has not created the socket yet, or the path differs. Wait for startup and check the path. |

## Output

The exact QEMU or libvirt command that ran, the guest console evidence (boot messages, breakpoint hit, or QMP answer), and the teardown list: processes to stop, snapshots or images to remove, domains to undefine, and devices to rebind to their original driver.
