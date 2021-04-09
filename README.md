# sammo(REGNET)
Python Based blockchiain network project focusing on scalability, faster transaction rate, low barrier of entry.

This network is fully functioning and capable of any transactions anonymously in a de-cenvtralized manner. But we don't recoomand it
as a final product. Instade it is foundation for building any blockchain network.
###Instructions:
1. Set node id :  `export NODE_ID=[node id]`. 
   you can choose any number for the [node id]. (`2000`, `3000`, `4000` etc.)
2. create wallet: `python main.py -CW`.
3. list address: `python main.py -L`.
4. create blockchain: `python main.py -CB [your address]`.
5. check balance: `python main.py -GB [your address]`.
6. send token: `python main.py -S [your amount] -T [your address] -F [receiver address]`.
   for instant mining of the new block without sending it to the network just add `--mine` at the end of above command.

Open up multiple windows of your preferred terminal. Follow step:1 and step:2 for each terminal.Create blockchain for one of those teminal(for the first time).

For more informaton: `python main.py --help`

### TO-DO:
Goal is to make a distributed Hyperledger to compete with current financial system in terms of scalability, cost of transaction, accessibility.
1. Make conversion between cross currency exchange more smoother.
