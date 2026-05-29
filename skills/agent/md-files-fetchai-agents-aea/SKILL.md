``` yaml
name: echo
authors: fetchai
version: 0.1.0
license: Apache-2.0
behaviours:
  echo:
    class_name: EchoBehaviour
    args:
      tick_interval: 1.0
handlers:
  echo:
    class_name: EchoHandler
    args:
      foo: bar
models: {}
dependencies: {}
protocols:
- fetchai/default:1.1.7
```

``` bash
aea scaffold error-handler
```
