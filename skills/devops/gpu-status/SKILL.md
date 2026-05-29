---
name: gpu-status
description: Check GPU allocation and utilization across all nodes. Use when asked about GPUs, VRAM, or model capacity.
allowed-tools: Bash
---

# GPU Status

Check GPU state across the cluster:

1. **GPU Allocation per Node**:
   ```bash
   kubectl describe nodes | node -e '
   let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>{
     const nodes=d.split("Name:");
     nodes.slice(1).forEach(n=>{
       const name=n.split("\n")[0].trim();
       const gpuCap=(n.match(/nvidia.com\/gpu:\s+(\d+)/g)||[]);
       console.log(name+":",gpuCap.join(", ")||"no GPUs");
     });
   })'
   ```

2. **Pods Using GPUs**:
   ```bash
   kubectl get pods -A -o json | node -e '
   let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>{
     const pods=JSON.parse(d).items;
     pods.forEach(p=>{
       const gpu=p.spec.containers.some(c=>c.resources&&c.resources.limits&&c.resources.limits["nvidia.com/gpu"]);
       if(gpu) console.log(p.metadata.namespace+"/"+p.metadata.name,"- GPU:",
         p.spec.containers.map(c=>(c.resources?.limits?.["nvidia.com/gpu"]||0)).join(","));
     });
   })'
   ```

3. **Live nvidia-smi** (if inference pods running):
   ```bash
   kubectl exec -n inference deploy/sglang-reasoning -- nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null || echo "Cannot exec into reasoning pod"
   ```

Report VRAM used vs available, which models are loaded, and remaining capacity.
