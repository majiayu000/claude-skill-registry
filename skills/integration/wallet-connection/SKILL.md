---
name: Wallet Connection
description: Enabling users to interact with dApps using their crypto wallets including MetaMask, WalletConnect, RainbowKit, and Wagmi integration for Web3 applications.
---

# Wallet Connection

> **Current Level:** Intermediate  
> **Domain:** Blockchain / Web3 / Frontend

---

## Overview

Wallet connection enables users to interact with dApps using their crypto wallets. This guide covers MetaMask, WalletConnect, RainbowKit, and Wagmi integration for building Web3 applications that connect to user wallets securely.

## Wallet Connection Patterns

```
User → Connect Wallet → Sign Message → Interact with dApp
```

**Popular Wallets:**
- MetaMask (Browser Extension)
- WalletConnect (Mobile)
- Coinbase Wallet
- Rainbow Wallet
- Trust Wallet

## MetaMask Integration

```typescript
// lib/metamask.ts
export class MetaMaskService {
  async connect(): Promise<string> {
    if (!window.ethereum) {
      throw new Error('MetaMask not installed');
    }

    const accounts = await window.ethereum.request({
      method: 'eth_requestAccounts'
    });

    return accounts[0];
  }

  async getAccounts(): Promise<string[]> {
    if (!window.ethereum) return [];

    return window.ethereum.request({
      method: 'eth_accounts'
    });
  }

  async switchChain(chainId: number): Promise<void> {
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: `0x${chainId.toString(16)}` }]
    });
  }

  async addChain(config: ChainConfig): Promise<void> {
    await window.ethereum.request({
      method: 'wallet_addEthereumChain',
      params: [{
        chainId: `0x${config.chainId.toString(16)}`,
        chainName: config.name,
        rpcUrls: [config.rpcUrl],
        nativeCurrency: config.nativeCurrency,
        blockExplorerUrls: [config.blockExplorer]
      }]
    });
  }

  onAccountsChanged(callback: (accounts: string[]) => void): () => void {
    window.ethereum.on('accountsChanged', callback);

    return () => {
      window.ethereum.removeListener('accountsChanged', callback);
    };
  }

  onChainChanged(callback: (chainId: string) => void): () => void {
    window.ethereum.on('chainChanged', callback);

    return () => {
      window.ethereum.removeListener('chainChanged', callback);
    };
  }
}

interface ChainConfig {
  chainId: number;
  name: string;
  rpcUrl: string;
  nativeCurrency: {
    name: string;
    symbol: string;
    decimals: number;
  };
  blockExplorer: string;
}
```

## WalletConnect v2

```typescript
// lib/walletconnect.ts
import { EthereumProvider } from '@walletconnect/ethereum-provider';

export class WalletConnectService {
  private provider: EthereumProvider | null = null;

  async connect(): Promise<string> {
    this.provider = await EthereumProvider.init({
      projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!,
      chains: [1], // Ethereum mainnet
      showQrModal: true,
      methods: ['eth_sendTransaction', 'personal_sign'],
      events: ['chainChanged', 'accountsChanged']
    });

    const accounts = await this.provider.enable();
    return accounts[0];
  }

  async disconnect(): Promise<void> {
    await this.provider?.disconnect();
    this.provider = null;
  }

  getProvider(): EthereumProvider | null {
    return this.provider;
  }

  onAccountsChanged(callback: (accounts: string[]) => void): void {
    this.provider?.on('accountsChanged', callback);
  }

  onChainChanged(callback: (chainId: number) => void): void {
    this.provider?.on('chainChanged', callback);
  }

  onDisconnect(callback: () => void): void {
    this.provider?.on('disconnect', callback);
  }
}
```

## RainbowKit

```typescript
// lib/rainbowkit-config.ts
import '@rainbow-me/rainbowkit/styles.css';
import { getDefaultWallets, RainbowKitProvider } from '@rainbow-me/rainbowkit';
import { configureChains, createConfig, WagmiConfig } from 'wagmi';
import { mainnet, polygon, optimism, arbitrum } from 'wagmi/chains';
import { alchemyProvider } from 'wagmi/providers/alchemy';
import { publicProvider } from 'wagmi/providers/public';

const { chains, publicClient } = configureChains(
  [mainnet, polygon, optimism, arbitrum],
  [
    alchemyProvider({ apiKey: process.env.NEXT_PUBLIC_ALCHEMY_KEY! }),
    publicProvider()
  ]
);

const { connectors } = getDefaultWallets({
  appName: 'My dApp',
  projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!,
  chains
});

const wagmiConfig = createConfig({
  autoConnect: true,
  connectors,
  publicClient
});

// _app.tsx
function MyApp({ Component, pageProps }: AppProps) {
  return (
    <WagmiConfig config={wagmiConfig}>
      <RainbowKitProvider chains={chains}>
        <Component {...pageProps} />
      </RainbowKitProvider>
    </WagmiConfig>
  );
}

// Usage in component
import { ConnectButton } from '@rainbow-me/rainbowkit';

function Header() {
  return (
    <header>
      <ConnectButton />
    </header>
  );
}
```

## Wagmi Hooks

```typescript
// hooks/useWallet.ts
import { useAccount, useConnect, useDisconnect, useNetwork, useSwitchNetwork } from 'wagmi';

export function useWallet() {
  const { address, isConnected } = useAccount();
  const { connect, connectors, isLoading } = useConnect();
  const { disconnect } = useDisconnect();
  const { chain } = useNetwork();
  const { switchNetwork } = useSwitchNetwork();

  return {
    address,
    isConnected,
    connect,
    disconnect,
    connectors,
    isLoading,
    chain,
    switchNetwork
  };
}

// Usage
function WalletButton() {
  const { address, isConnected, connect, disconnect, connectors } = useWallet();

  if (isConnected) {
    return (
      <div>
        <p>Connected: {address}</p>
        <button onClick={() => disconnect()}>Disconnect</button>
      </div>
    );
  }

  return (
    <div>
      {connectors.map((connector) => (
        <button
          key={connector.id}
          onClick={() => connect({ connector })}
        >
          Connect {connector.name}
        </button>
      ))}
    </div>
  );
}
```

### More Wagmi Hooks

```typescript
// hooks/useBalance.ts
import { useBalance } from 'wagmi';

export function useWalletBalance(address?: string) {
  const { data, isLoading, refetch } = useBalance({
    address: address as `0x${string}`,
    watch: true
  });

  return {
    balance: data?.formatted,
    symbol: data?.symbol,
    isLoading,
    refetch
  };
}

// hooks/useENS.ts
import { useEnsName, useEnsAvatar } from 'wagmi';

export function useENS(address?: string) {
  const { data: ensName } = useEnsName({
    address: address as `0x${string}`
  });

  const { data: ensAvatar } = useEnsAvatar({
    name: ensName
  });

  return { ensName, ensAvatar };
}

// hooks/useTransaction.ts
import { useSendTransaction, useWaitForTransaction } from 'wagmi';

export function useSendEther() {
  const { data, sendTransaction } = useSendTransaction();
  const { isLoading, isSuccess } = useWaitForTransaction({
    hash: data?.hash
  });

  const send = (to: string, value: string) => {
    sendTransaction({
      to: to as `0x${string}`,
      value: parseEther(value)
    });
  };

  return { send, isLoading, isSuccess, hash: data?.hash };
}
```

## Account Management

```typescript
// services/account.service.ts
export class AccountService {
  async getBalance(address: string, provider: ethers.providers.Provider): Promise<string> {
    const balance = await provider.getBalance(address);
    return ethers.utils.formatEther(balance);
  }

  async getTokenBalance(
    address: string,
    tokenAddress: string,
    provider: ethers.providers.Provider
  ): Promise<string> {
    const abi = ['function balanceOf(address) view returns (uint256)'];
    const contract = new ethers.Contract(tokenAddress, abi, provider);
    const balance = await contract.balanceOf(address);
    return ethers.utils.formatUnits(balance, 18);
  }

  async getTransactionHistory(
    address: string,
    provider: ethers.providers.Provider
  ): Promise<Transaction[]> {
    const currentBlock = await provider.getBlockNumber();
    const history: Transaction[] = [];

    // Get last 100 blocks
    for (let i = currentBlock; i > currentBlock - 100; i--) {
      const block = await provider.getBlockWithTransactions(i);
      
      block.transactions.forEach(tx => {
        if (tx.from === address || tx.to === address) {
          history.push({
            hash: tx.hash,
            from: tx.from,
            to: tx.to || '',
            value: ethers.utils.formatEther(tx.value),
            blockNumber: tx.blockNumber || 0
          });
        }
      });
    }

    return history;
  }
}

interface Transaction {
  hash: string;
  from: string;
  to: string;
  value: string;
  blockNumber: number;
}
```

## Network Switching

```typescript
// components/NetworkSwitcher.tsx
import { useSwitchNetwork, useNetwork } from 'wagmi';

export function NetworkSwitcher() {
  const { chain } = useNetwork();
  const { chains, switchNetwork } = useSwitchNetwork();

  return (
    <div>
      <p>Current Network: {chain?.name}</p>
      <select
        value={chain?.id}
        onChange={(e) => switchNetwork?.(Number(e.target.value))}
      >
        {chains.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}
      </select>
    </div>
  );
}
```

## Signature Requests

```typescript
// services/signature.service.ts
export class SignatureService {
  async signMessage(
    message: string,
    signer: ethers.Signer
  ): Promise<string> {
    return signer.signMessage(message);
  }

  async signTypedData(
    domain: ethers.TypedDataDomain,
    types: Record<string, ethers.TypedDataField[]>,
    value: Record<string, any>,
    signer: ethers.Signer
  ): Promise<string> {
    return signer._signTypedData(domain, types, value);
  }

  verifyMessage(
    message: string,
    signature: string
  ): string {
    return ethers.utils.verifyMessage(message, signature);
  }

  verifyTypedData(
    domain: ethers.TypedDataDomain,
    types: Record<string, ethers.TypedDataField[]>,
    value: Record<string, any>,
    signature: string
  ): string {
    return ethers.utils.verifyTypedData(domain, types, value, signature);
  }
}

// Usage with Wagmi
import { useSignMessage } from 'wagmi';

function SignMessageButton() {
  const { signMessage, data, isLoading } = useSignMessage({
    message: 'Hello Web3!'
  });

  return (
    <div>
      <button onClick={() => signMessage()} disabled={isLoading}>
        Sign Message
      </button>
      {data && <p>Signature: {data}</p>}
    </div>
  );
}
```

## Error Handling

```typescript
// utils/wallet-errors.ts
export class WalletErrorHandler {
  static handle(error: any): string {
    // User rejected
    if (error.code === 4001) {
      return 'User rejected the request';
    }

    // Chain not added
    if (error.code === 4902) {
      return 'Chain not added to wallet';
    }

    // Unauthorized
    if (error.code === 4100) {
      return 'Unauthorized - please connect wallet';
    }

    // Unsupported method
    if (error.code === 4200) {
      return 'Unsupported method';
    }

    // Disconnected
    if (error.code === 4900) {
      return 'Wallet disconnected';
    }

    // Chain disconnected
    if (error.code === 4901) {
      return 'Chain disconnected';
    }

    return error.message || 'Unknown wallet error';
  }
}
```

## Mobile Wallet Support

```typescript
// utils/mobile-wallet.ts
export function isMobile(): boolean {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}

export function openWalletApp(uri: string): void {
  if (isMobile()) {
    // Deep link to wallet app
    const walletLinks = {
      metamask: `https://metamask.app.link/dapp/${window.location.host}`,
      trust: `trust://open_url?url=${encodeURIComponent(window.location.href)}`,
      rainbow: `rainbow://wc?uri=${encodeURIComponent(uri)}`
    };

    // Try to open MetaMask
    window.location.href = walletLinks.metamask;
  }
}

// Mobile-optimized connection
export async function connectMobileWallet(): Promise<string> {
  if (isMobile() && !window.ethereum) {
    // Redirect to MetaMask app
    openWalletApp('');
    throw new Error('Opening wallet app...');
  }

  // Normal connection
  const accounts = await window.ethereum.request({
    method: 'eth_requestAccounts'
  });

  return accounts[0];
}
```

## UX Best Practices

```typescript
// components/WalletConnection.tsx
export function WalletConnection() {
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string>('');

  const connect = async () => {
    setIsConnecting(true);
    setError('');

    try {
      await connectWallet();
    } catch (err: any) {
      setError(WalletErrorHandler.handle(err));
    } finally {
      setIsConnecting(false);
    }
  };

  return (
    <div>
      <button onClick={connect} disabled={isConnecting}>
        {isConnecting ? (
          <>
            <Spinner /> Connecting...
          </>
        ) : (
          'Connect Wallet'
        )}
      </button>

      {error && (
        <div className="error">
          {error}
          <button onClick={() => setError('')}>Dismiss</button>
        </div>
      )}
    </div>
  );
}

// Show network indicator
export function NetworkIndicator() {
  const { chain } = useNetwork();
  const isWrongNetwork = chain?.id !== 1; // Not mainnet

  if (isWrongNetwork) {
    return (
      <div className="warning">
        ⚠️ Please switch to Ethereum Mainnet
      </div>
    );
  }

  return (
    <div className="network-badge">
      {chain?.name}
    </div>
  );
}
```

## Best Practices

1. **Auto-Connect** - Remember user's wallet choice
2. **Error Handling** - Handle all wallet errors gracefully
3. **Network Detection** - Detect and handle wrong networks
4. **Mobile Support** - Support mobile wallets
5. **Loading States** - Show loading indicators
6. **Disconnect** - Provide clear disconnect option
7. **Multi-Wallet** - Support multiple wallet types
8. **Security** - Never request private keys
9. **UX** - Clear connection status
10. **Testing** - Test with different wallets

---

## Quick Start

### RainbowKit Setup

```bash
npm install @rainbow-me/rainbowkit wagmi viem
```

```tsx
import { RainbowKitProvider, getDefaultWallets } from '@rainbow-me/rainbowkit'
import { configureChains, createConfig, WagmiConfig } from 'wagmi'
import { mainnet, polygon } from 'wagmi/chains'
import { publicProvider } from 'wagmi/providers/public'

const { chains, publicClient } = configureChains(
  [mainnet, polygon],
  [publicProvider()]
)

const { connectors } = getDefaultWallets({
  appName: 'My App',
  projectId: 'YOUR_PROJECT_ID',
  chains
})

const wagmiConfig = createConfig({
  autoConnect: true,
  connectors,
  publicClient
})

function App() {
  return (
    <WagmiConfig config={wagmiConfig}>
      <RainbowKitProvider chains={chains}>
        <YourApp />
      </RainbowKitProvider>
    </WagmiConfig>
  )
}
```

---

## Production Checklist

- [ ] **Wallet Support**: Support multiple wallets (MetaMask, WalletConnect)
- [ ] **Network Support**: Support multiple networks (Mainnet, Polygon, etc.)
- [ ] **Connection Status**: Show connection status
- [ ] **Account Display**: Display connected account
- [ ] **Network Switching**: Allow network switching
- [ ] **Error Handling**: Handle connection errors
- [ ] **Security**: Never request private keys
- [ ] **UX**: Clear connection flow
- [ ] **Testing**: Test with different wallets
- [ ] **Documentation**: Document wallet integration
- [ ] **Monitoring**: Monitor connection issues
- [ ] **Fallback**: Fallback for unsupported wallets

---

## Anti-patterns

### ❌ Don't: Request Private Keys

```javascript
// ❌ Bad - Request private key
const privateKey = prompt('Enter private key')  // NEVER!
```

```javascript
// ✅ Good - Use wallet provider
const { data: account } = useAccount()  // Wallet handles keys
```

### ❌ Don't: No Error Handling

```javascript
// ❌ Bad - No error handling
const account = await connect()  // What if user rejects?
```

```javascript
// ✅ Good - Handle errors
try {
  const account = await connect()
} catch (error) {
  if (error.code === 4001) {
    // User rejected connection
    showMessage('Connection rejected')
  } else {
    // Other error
    showError('Connection failed')
  }
}
```

---

## Integration Points

- **Web3 Integration** (`35-blockchain-web3/web3-integration/`) - Web3 patterns
- **Smart Contracts** (`35-blockchain-web3/smart-contracts/`) - Contract interaction
- **Blockchain Authentication** (`35-blockchain-web3/blockchain-authentication/`) - Auth patterns

---

## Further Reading

- [RainbowKit](https://www.rainbowkit.com/)
- [Wagmi](https://wagmi.sh/)
- [WalletConnect](https://walletconnect.com/)
- [MetaMask Docs](https://docs.metamask.io/)
