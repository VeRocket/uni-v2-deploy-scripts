# ZumoSwap Deployement Tools.

Clone from VeChain Community open source code.

https://github.com/VeChainDEXCode/uni-v2-deploy-scripts

## How TO

Read the `Makefile` first before execute below commands.

### Install depedencies
```bash
make install
```

### Deploy vVET
```bash
make deploy_vvet network={http://url} \
    private={private_key} \
    vvet={/path/to/vvet.json} 
```

### Deploy Factory + Router 02 of Uni v2
```bash
make deploy_univ2 network={http://url} \
    private={private_key} \
    factory={/path/to/UniswapV2Factory.json} \
    router={/path/to/UniswapV2Router02.json} \
    vvetaddress={0x....}
```

### Create Pool of vVET + VTHO
```bash
make create_pool network={http://url} \
    private={private_key} \
    factory={/path/to/UniswapV2Factory.json} \
    factoryaddress={0x...} \
    vvetaddress={0x...} \
    vthoaddress={0x...}
```

### Deposit intial funds of VET+VTHO into Pool
```bash
make deposit_funds network={http://url} \
    private={private_key} \
    router={/path/to/Router02.json} \
    routeraddress={0x...} \
    vvetaddress={0x...} \
    vthoaddress={0x...} \
    vvet={/path/to/vvet.json} \
    vetamount={123456} \
    vthoamount={123456}
```

## Disclaimer (I)

- This repo keeps the upstream license of GPL-3.0.
- Neither the name of ZumoSwap nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.


## Disclaimer (II)
Redistributions of source code must retain this list of conditions and the following disclaimer.

Neither the name of VeChain (VeChain Foundation) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
