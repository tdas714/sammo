# sammo(REGNET)
Python Based AI based peer-to-peer payment system.

This network is fully functioning and capable of any transactions anonymously in a de-cenvtralized manner. But I don't recoomand it
as a final product. Instade it is foundation for building any blockchain network.
###Instructions:
1. Set node id :  `export NODE_ID=[node id]` 
   you can choose any number for the [node id]. (`2000`, `3000`, `4000` etc.)
2. create wallet: `python main.py -CW`
3. create blockchain:(This is for the first time.You don't have to create blockchain everytime) 
   `python main.py -CB`
4. list address: `python main.py -L`
5. check balance: `python main.py -GB [your address]`
6. send token: `python main.py -S [your amount] -T [your address] -F [receiver address]`
   for inbstant mining of the new block without sending it to the network just add `--mine` at the end of above command.

Open up multiple windows of your preferred terminal. Follow step:1 and step:2 for each terminal.Create blockchain for one of those teminal(for the first time).

For more informaton: `python main.py --help`

### TO-DO:
1. Implement ML for consensus algorithm.
