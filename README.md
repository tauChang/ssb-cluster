# ssb-cluster

## Instruction
* Copy the manifest of your CloudLab cluster into `manifest.xml`
* Control the nodes in `main()`. For example, `users["node-0"].follow(users["node-0"])`. You can implement more methods in `user.py`!
* Run `python main.py --manifest manifest.xml --setup-node 1`. The `--setup-node` option is needed when you first deploy SSB on the cluster. If you are reusing the cluster later, you do not need to do node setup again.