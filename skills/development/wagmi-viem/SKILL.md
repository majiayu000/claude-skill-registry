---
name: wagmi-viem
description: Web3 integration with wagmi and viem - wallet connection, contract interactions, transactions, RainbowKit. Use when implementing wallet features, reading/writing contracts, or handling blockchain transactions.
---

# Wagmi & Viem - Web3 Integration

## Setup with RainbowKit

```tsx
// _app.tsx
import '@rainbow-me/rainbowkit/styles.css'
import { getDefaultConfig, RainbowKitProvider } from '@rainbow-me/rainbowkit'
import { WagmiProvider } from 'wagmi'
import { base, baseSepolia } from 'wagmi/chains'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const config = getDefaultConfig({
  appName: 'Kardashev Network',
  projectId: 'YOUR_PROJECT_ID',  // Get from cloud.walletconnect.com
  chains: [base, baseSepolia],
})

const queryClient = new QueryClient()

function App({ Component, pageProps }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>
          <Component {...pageProps} />
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

## Connect Button

```tsx
import { ConnectButton } from '@rainbow-me/rainbowkit'

function Header() {
  return (
    <nav>
      <ConnectButton />
      {/* Or custom */}
      <ConnectButton.Custom>
        {({ account, chain, openConnectModal, mounted }) => {
          if (!mounted || !account || !chain) {
            return <button onClick={openConnectModal}>Connect</button>
          }
          return <span>{account.displayName}</span>
        }}
      </ConnectButton.Custom>
    </nav>
  )
}
```

## Account & Chain Hooks

```tsx
import { useAccount, useChainId, useBalance, useEnsName } from 'wagmi'

function Profile() {
  const { address, isConnected, isConnecting } = useAccount()
  const chainId = useChainId()
  const { data: balance } = useBalance({ address })
  const { data: ensName } = useEnsName({ address })

  if (!isConnected) return <div>Not connected</div>

  return (
    <div>
      <p>Address: {ensName || address}</p>
      <p>Balance: {balance?.formatted} {balance?.symbol}</p>
      <p>Chain: {chainId}</p>
    </div>
  )
}
```

## Read Contract

```tsx
import { useReadContract, useReadContracts } from 'wagmi'

// Single read
function TokenBalance() {
  const { data, isLoading, error } = useReadContract({
    address: '0x...',
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: ['0xUserAddress...'],
  })

  if (isLoading) return <div>Loading...</div>
  return <div>Balance: {data?.toString()}</div>
}

// Multiple reads
function MultipleReads() {
  const { data } = useReadContracts({
    contracts: [
      { address: '0x...', abi, functionName: 'totalSupply' },
      { address: '0x...', abi, functionName: 'name' },
      { address: '0x...', abi, functionName: 'symbol' },
    ],
  })
}
```

## Write Contract

```tsx
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi'

function MintButton() {
  const { writeContract, data: hash, isPending, error } = useWriteContract()

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  })

  const handleMint = () => {
    writeContract({
      address: '0x...',
      abi: contractAbi,
      functionName: 'mint',
      args: [amount],
      value: parseEther('0.01'),  // If payable
    })
  }

  return (
    <div>
      <button onClick={handleMint} disabled={isPending}>
        {isPending ? 'Confirming...' : 'Mint'}
      </button>
      {isConfirming && <div>Waiting for confirmation...</div>}
      {isSuccess && <div>Success! Hash: {hash}</div>}
      {error && <div>Error: {error.message}</div>}
    </div>
  )
}
```

## Prepare + Write Pattern

```tsx
import { useSimulateContract, useWriteContract } from 'wagmi'

function PreparedWrite() {
  const { data: simulation } = useSimulateContract({
    address: '0x...',
    abi,
    functionName: 'transfer',
    args: [recipientAddress, amount],
  })

  const { writeContract } = useWriteContract()

  const handleClick = () => {
    if (simulation?.request) {
      writeContract(simulation.request)
    }
  }

  return <button onClick={handleClick}>Transfer</button>
}
```

## Watch Contract Events

```tsx
import { useWatchContractEvent } from 'wagmi'

function EventWatcher() {
  useWatchContractEvent({
    address: '0x...',
    abi,
    eventName: 'Transfer',
    onLogs(logs) {
      logs.forEach((log) => {
        console.log('Transfer:', log.args.from, log.args.to, log.args.value)
      })
    },
  })
}
```

## Sign Message

```tsx
import { useSignMessage } from 'wagmi'

function SignMessage() {
  const { signMessage, data: signature, isPending } = useSignMessage()

  return (
    <button onClick={() => signMessage({ message: 'Hello World' })}>
      {isPending ? 'Signing...' : 'Sign Message'}
    </button>
  )
}
```

## Switch Chain

```tsx
import { useSwitchChain } from 'wagmi'

function ChainSwitcher() {
  const { chains, switchChain, isPending } = useSwitchChain()

  return (
    <div>
      {chains.map((chain) => (
        <button
          key={chain.id}
          onClick={() => switchChain({ chainId: chain.id })}
          disabled={isPending}
        >
          {chain.name}
        </button>
      ))}
    </div>
  )
}
```

## Viem Utilities

```tsx
import { formatEther, parseEther, formatUnits, parseUnits } from 'viem'

// ETH formatting
formatEther(1000000000000000000n)  // "1"
parseEther('1')                     // 1000000000000000000n

// Token formatting (6 decimals for USDC)
formatUnits(1000000n, 6)  // "1"
parseUnits('1', 6)        // 1000000n

// Address utilities
import { isAddress, getAddress } from 'viem'
isAddress('0x...')         // boolean
getAddress('0x...')        // Checksummed address
```

## Custom Hook Pattern

```tsx
import { useReadContract, useWriteContract, useAccount } from 'wagmi'

export function useKardashevContract() {
  const { address } = useAccount()

  const { data: balance } = useReadContract({
    address: CONTRACT_ADDRESS,
    abi: CONTRACT_ABI,
    functionName: 'balanceOf',
    args: [address],
    query: { enabled: !!address },
  })

  const { writeContract, isPending } = useWriteContract()

  const mint = (amount: bigint) => {
    writeContract({
      address: CONTRACT_ADDRESS,
      abi: CONTRACT_ABI,
      functionName: 'mint',
      args: [amount],
    })
  }

  return { balance, mint, isPending }
}
```

## Error Handling

```tsx
import { BaseError, ContractFunctionRevertedError } from 'viem'

function handleError(error: Error) {
  if (error instanceof BaseError) {
    const revertError = error.walk(e => e instanceof ContractFunctionRevertedError)
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName
      console.log('Contract reverted:', errorName)
    }
  }
}
```

## TypeScript Contract Types

```tsx
// Generate types from ABI
const abi = [...] as const  // Use 'as const' for type inference

// Or use abitype
import { Abi } from 'abitype'
const abi: Abi = [...]
```
