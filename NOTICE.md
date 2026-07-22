# Attribution Notice

This project contains code derived from:

- Project: `capitan01R/ComfyUI-Krea2T-Enhancer`
- Upstream URL: https://github.com/capitan01R/ComfyUI-Krea2T-Enhancer
- Upstream revision reviewed: `0ed1fe2c658132d3c97e5ae2ede490324afc7d0b`
- License: MIT
- Original copyright: Copyright (c) 2026 capitan01R

Tutu-maintained changes in version 1.0.0:

- replaced the fixed diffusion-wrapper signature with transparent `*args, **kwargs` forwarding;
- added compatibility lookup for positional and keyword `transformer_options`;
- assigned independent node, wrapper, and configuration keys to avoid conflicts;
- added regression tests for the old and new ComfyUI Krea2 call shapes;
- changed user-facing names and diagnostics to identify the maintained node.

The Krea2 enhancement algorithm and control semantics remain derived from the upstream implementation.
