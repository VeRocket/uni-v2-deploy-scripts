SHELL=/bin/bash

export network=http://localhost:8669
export private=99f0500549792796c14fed62011a51081dc5b5e68fe8bd8a13b86be829c4fd36 # address: 0xf077b491b355e64048ce21e3a6fc4751eeea77fa
export vvet=./external/VVET9.json
export factory=./external/UniswapV2Factory.json
export router=./external/UniswapV2Router02.json
export compiledfile=./external/UniswapV2Pair.json
export vvetaddress=''
export vthoaddress=0x0000000000000000000000000000456e65726779
export factoryaddress=''
export routeraddress=''
export vetamount=100000000000000000000  # 100 VET
export vthoamount=100000000000000000000 # 100 VTHO

# install compiler tools
install:
	python3 -m venv .env
	. .env/bin/activate && pip3 install wheel
	. .env/bin/activate && pip3 install -r requirements.txt

# Deploy VVET to the network you choose
deploy_vvet:
	. .env/bin/activate && python3 deploy_vvet.py $(network) $(private) $(vvet)

# Deploy Uni V2 to the network you choose
deploy_univ2:
	. .env/bin/activate && python3 deploy_univ2.py $(network) $(private) $(factory) $(router) $(vvetaddress)

# Create Pools between vVET and VTHO (call factory.sol)
create_pool:
	. .env/bin/activate && python3 create_pool.py $(network) $(private) $(factory) $(factoryaddress) $(vvetaddress) $(vthoaddress)

# Deposit initial funds of VET and VTHO to the pool (call router02.sol)
deposit_funds:
	. .env/bin/activate && python3 deposit_funds.py $(network) $(private) $(router) $(routeraddress) $(vvetaddress) $(vthoaddress) $(vvet) $(vetamount) $(vthoamount)