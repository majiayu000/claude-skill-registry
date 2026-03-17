---
category: Business
id: x402-client

name: X402 Client

description: End-to-end Celo development playbook (Feb 2026). Prefer viem for all client/transaction code (native fee currency support via CIP-64). Use thirdweb for wallet connection and React dApps. Foundry for smart contract development. Covers fee abstraction (pay gas in USDC/USDT/USDm), MiniPay Mini Apps, stablecoin integration, and AI agent infrastructure (ERC-8004 trust + x402 payments).

user-invocable: true 

---

# Celo Development Skill (viem-first)  



## What this Skill is for  



Use this Skill when the user asks for: 

- Celo dApp UI work (React / Next.js) 

- Wallet connection + fee currency selection 

- Transactions paying gas in stablecoins (USDC, USDT, USDm) 

- MiniPay Mini App development 

- Smart contract development, testing, and deployment 

- Stablecoin integration (Mento + bridged) 

- AI agent infrastructure (ERC-8004 identity/reputation, x402 payments)



## Default stack decisions (opinionated)  



### 1. Client SDK: viem first



- **viem is REQUIRED** for fee abstraction (ethers.js/web3.js don't support `feeCurrency`) 

- Use `viem/celo` for Celo-specific transaction serialization 

- Never use ethers.js for new Celo projects  



```typescript 

import { createWalletClient, custom } from "viem"; 

import { celo } from "viem/chains";  



const walletClient = createWalletClient({   

  chain: celo,   

  transport: custom(window.ethereum), 

}); 

```



### 2. UI & Wallets: thirdweb  



- Use thirdweb SDK for wallet connection and React components 

- `ConnectButton` supports 500+ wallets including MiniPay 

- Built-in support for Celo chains  



```typescript 

import { ConnectButton } from "thirdweb/react"; 

import { celo } from "thirdweb/chains";  



<ConnectButton client={client} chain={celo} /> 

``` 



### 3. Fee Abstraction: always offer stablecoin gas  



Celo's killer feature: pay gas fees in ERC-20 tokens without paymasters or relayers.  



- Use **adapter addresses** for 6-decimal tokens (USDC, USDT) - adapters normalize decimals 

- Use **token addresses** directly for 18-decimal tokens (USDm, EURm, REALm) - no adapter needed 

- Requires viem (ethers.js/web3.js don't support `feeCurrency`) 

- Only works with Celo-native wallets (MiniPay) or custom implementations  



```typescript 

import { serializeTransaction } from "viem/celo"; 

import { parseGwei, parseEther } from "viem";  



// For 6-decimal tokens (USDC, USDT): use ADAPTER address 

const USDC_ADAPTER = "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B";  



// For 18-decimal tokens (USDm, EURm): use TOKEN address directly 

const USDM_TOKEN = "0x765DE816845861e75A25fCA122bb6898B8B1282a";  



const serialized = serializeTransaction({   

  chainId: 42220,   

  gas: 21001n,   

  feeCurrency: USDC_ADAPTER, // or USDM_TOKEN for USDm   

  maxFeePerGas: parseGwei("20"),   

  maxPriorityFeePerGas: parseGwei("2"),   

  nonce: 69,   

  to: "0x1234512345123451234512345123451234512345",   

  value: parseEther("0.01"), 

}); 

```



### 4. Smart Contracts: Foundry  



- Use Foundry (forge, cast, anvil) for all contract development 

- Fast compilation, powerful testing, built-in fuzzing 

- Native Celo verification support via Celoscan API  



```bash 

# Install Foundry 

curl -L https://foundry.paradigm.xyz | bash && foundryup  



# Create project 

forge init my-project && cd my-project  



# Deploy to Celo Sepolia 

forge script script/Deploy.s.sol \   

  --rpc-url https://forno.celo-sepolia.celo-testnet.org \   

  --broadcast --verify 

```



### 5. MiniPay: mobile-first stablecoin UX  



- Detect MiniPay via `window.ethereum?.isMiniPay` 

- Users have stablecoins (USDm, USDC), not CELO 

- Hide "Connect Wallet" button - connection is implicit 

- Test via MiniPay Site Tester with ngrok  



```typescript 

function isMiniPay(): boolean {   

  return typeof window !== "undefined" &&          

      window.ethereum?.isMiniPay === true; 

} 

```



### 6. AI Agents: ERC-8004 + x402  



For AI agent development on Celo: 

- **ERC-8004**: On-chain identity, reputation, and trust verification 

- **x402**: HTTP-native micropayments with stablecoins  



```typescript 

// Verify agent trust before interaction 

const summary = await reputationRegistry.getSummary(agentId); 

if (summary.averageScore >= 80) {   

  // Make paid request to trusted agent   

  const response = await fetchWithPayment(serviceUrl); 

} 

```



## Operating procedure  



### 1. Classify the task layer  



| Layer | Tools | 

|-------|-------| 

| UI/wallet/hooks | viem + thirdweb | 

| Scripts/backend | viem directly | 

| Smart contracts | Foundry (forge) | 

| MiniPay apps | MiniPay detection + stablecoin UX | 

| AI agents | ERC-8004 + x402 |



### 2. Pick the right fee currency approach  



| Scenario | Approach | 

|----------|----------| 

| User has MiniPay | Offer fee currency selection | 

| User has MetaMask | Must pay in CELO (no fee abstraction) | 

| Server-side/scripts | Always use fee currency with viem |



### 3. Implement with Celo-specific correctness  



Always be explicit about: 

- **Network**: Mainnet (42220) vs Sepolia (11142220) 

- **Fee currency**: Adapter address (6-decimal) vs token address (18-decimal) 

- **Wallet compatibility**: MiniPay supports fee abstraction, MetaMask does not



### 4. Add tests  



- Test both CELO and fee currency transactions separately 

- Test wallet connection with MiniPay detection 

- For contracts, use `forge test` with fuzzing 

- For MiniPay apps, test in Site Tester on real device



### 5. Deliverables  



When implementing changes, provide: 

- Exact files changed 

- Commands to install/build/test/deploy 

- Fee currency addresses used (mainnet vs testnet) 

- Wallet compatibility notes 



## Quick reference  



### Networks  



| Network | Chain ID | RPC Endpoint | Explorer | 

|---------|----------|--------------|----------| 

| Mainnet | 42220 | https://forno.celo.org | https://celoscan.io | 

| Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org | https://sepolia.celoscan.io |



### Fee Currency Addresses - Mainnet  



**Why adapters?** Celo's gas calculations use 18 decimals internally. Tokens with different decimals (like USDC/USDT with 6 decimals) need adapter contracts to normalize the decimal conversion. Native Mento stablecoins (USDm, EURm, REALm) are already 18 decimals, so you use their token address directly.



| Token | Decimals | feeCurrency Address | Type | 

|-------|----------|---------------------|------| 

| USDC | 6 | 0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B | Adapter | 

| USDT | 6 | 0x0e2a3e05bc9a16f5292a6170456a710cb89c6f72 | Adapter | 

| USDm | 18 | 0x765DE816845861e75A25fCA122bb6898B8B1282a | Token (no adapter needed) | 

| EURm | 18 | 0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73 | Token (no adapter needed) | 

| REALm | 18 | 0xe8537a3d056DA446677B9E9d6c5dB704EaAb4787 | Token (no adapter needed) |



### Fee Currency Addresses - Celo Sepolia  



| Token | Decimals | feeCurrency Address | Type | 

|-------|----------|---------------------|------| 

| USDC | 6 | 0x4822e58de6f5e485eF90df51C41CE01721331dC0 | Adapter | 

| USDm | 18 | 0xdE9e4C3ce781b4bA68120d6261cbad65ce0aB00b | Token (no adapter needed) | 

| EURm | 18 | 0xA99dC247d6b7B2E3ab48a1fEE101b83cD6aCd82a | Token (no adapter needed) | 



### Core Protocol Contracts - Mainnet  



| Contract | Address | 

|----------|---------| 

| CELO Token | 0x471EcE3750Da237f93B8E339c536989b8978a438 | 

| FeeCurrencyDirectory | 0x15F344b9E6c3Cb6F0376A36A64928b13F62C6276 | 

| Registry | 0x000000000000000000000000000000000000ce10 |



### Stablecoin Tokens - Mainnet  



| Token | Address | Decimals | 

|-------|---------|----------| 

| USDm | 0x765DE816845861e75A25fCA122bb6898B8B1282a | 18 | 

| EURm | 0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73 | 18 | 

| USDC | 0xcebA9300f2b948710d2653dD7B07f33A8B32118C | 6 | 

| USDT | 0x48065fbbe25f71c9282ddf5e1cd6d6a887483d5e | 6 | 





## Progressive disclosure (read when needed)  



Detailed documentation for each topic is available in the [celo-org/agent-skills](https://github.com/celo-org/agent-skills) repository:



### Client & Frontend 

- [viem](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/viem/SKILL.md) - TypeScript client with fee currency support 

- [wagmi](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/wagmi/SKILL.md) - React hooks for Celo dApps 

- [thirdweb](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/thirdweb/SKILL.md) - Full-stack Web3 development 

- [evm-wallet-integration](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/evm-wallet-integration/SKILL.md) - Wallet connection patterns



### Celo Features 

- [fee-abstraction](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/fee-abstraction/SKILL.md) - Pay gas with stablecoins 

- [minipay-integration](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/minipay-integration/SKILL.md) - MiniPay Mini App development 

- [celo-stablecoins](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/celo-stablecoins/SKILL.md) - USDT, USDC, USDm, EURm, BRLm, XOFm, KESm, PHPm, COPm, NGNm, GHSm, GBPm, ZARm, CADm, AUDm, CHFm, JPYm, BRLA, VCHF, VEUR, VGBP, USDGLO, agEURA + COPM

- [celo-rpc](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/celo-rpc/SKILL.md) - Blockchain interaction via RPC



### Smart Contracts 

- [evm-foundry](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/evm-foundry/SKILL.md) - Foundry development (recommended) 

- [contract-verification](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/contract-verification/SKILL.md) - Celoscan, Blockscout, Sourcify



### AI Agent Infrastructure 

- [8004](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/8004/SKILL.md) - ERC-8004 Agent Trust Protocol 

- [x402](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/x402/SKILL.md) - HTTP-native agent payments



### DeFi & Bridging 

- [celo-defi](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/celo-defi/SKILL.md) - DeFi protocol integration 

- [bridging](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/bridging/SKILL.md) - Asset bridging to/from Celo



### Scaffolding 

- [celo-composer](https://raw.githubusercontent.com/celo-org/agent-skills/main/skills/celo-composer/SKILL.md) - Project templates and scaffolding



## Official Documentation  

- [Token Contracts](https://docs.celo.org/tooling/contracts/token-contracts) - All token addresses 

- [Core Contracts](https://docs.celo.org/tooling/contracts/core-contracts) - Protocol contract addresses 

- [Fee Currency](https://docs.celo.org/developer/fee-currency) - Fee abstraction guide 

- [MiniPay](https://docs.celo.org/build-with-celo/minipay) - Mini App development 



## Why Celo?  

- **Fee abstraction**: Pay gas in stablecoins without paymasters 

- **Sub-second finality**: ~1 second block times 

- **Low fees**: Gas costs under $0.001 

- **Mobile-first**: MiniPay with 12.6M activations 

- **AI-native**: ERC-8004 trust + x402 payments built for agents 

- **Stablecoin ecosystem**: Native USDT, USDC, USDm, EURm, BRLm, XOFm, KESm, PHPm, COPm, NGNm, GHSm, GBPm, ZARm, CADm, AUDm, CHFm, JPYm, BRLA, VCHF, VEUR, VGBP, USDGLO, agEURA + COPM
