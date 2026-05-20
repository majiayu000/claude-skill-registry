---
name: dojo-token
description: Implement, deploy, and index ERC20 and ERC721 tokens in Dojo. Use when adding token contracts, deploying them, or configuring Torii to index balances and transfers.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Dojo Tokens

Implement ERC20/ERC721 tokens in Cairo, deploy them alongside your Dojo world, and configure Torii to index balances, transfers, and metadata.

## When to Use This Skill

- "Implement ERC20 token for game currency"
- "Create NFT items with ERC721"
- "Deploy an ERC20 token with my world"
- "Index token balances with Torii"
- "Query token transfers"
- "Use Origami for tokens"

## What This Skill Does

- Implement ERC20 fungible tokens and ERC721 NFTs in Cairo
- Deploy token contracts as external contracts via `sozo migrate`
- Configure Torii to index token balances, transfers, and metadata
- Query token data via SQL and client SDKs

## Using Origami Library

Add to `Scarb.toml`:
```toml
[dependencies]
origami_token = { git = "https://github.com/dojoengine/origami", tag = "v1.0.0" }
```

Origami provides reusable token components following standard interfaces.
Refer to the [Origami documentation](https://github.com/dojoengine/origami) for the latest API.

## Simple Token Implementation

You can implement tokens using standard Dojo models without Origami.

### ERC20-like Currency

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Gold {
    #[key]
    pub player: ContractAddress,
    pub amount: u256,
}

#[starknet::interface]
trait IGoldToken<T> {
    fn mint(ref self: T, to: ContractAddress, amount: u256);
    fn transfer(ref self: T, to: ContractAddress, amount: u256);
    fn balance_of(self: @T, account: ContractAddress) -> u256;
}

#[dojo::contract]
mod gold_token {
    use super::{IGoldToken, Gold};
    use starknet::{ContractAddress, get_caller_address};
    use dojo::model::ModelStorage;

    #[abi(embed_v0)]
    impl GoldTokenImpl of IGoldToken<ContractState> {
        fn mint(ref self: ContractState, to: ContractAddress, amount: u256) {
            let mut world = self.world_default();

            let mut balance: Gold = world.read_model(to);
            balance.amount += amount;
            world.write_model(@balance);
        }

        fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) {
            let mut world = self.world_default();
            let from = get_caller_address();

            let mut from_balance: Gold = world.read_model(from);
            let mut to_balance: Gold = world.read_model(to);

            assert(from_balance.amount >= amount, 'insufficient balance');

            from_balance.amount -= amount;
            to_balance.amount += amount;

            world.write_model(@from_balance);
            world.write_model(@to_balance);
        }

        fn balance_of(self: @ContractState, account: ContractAddress) -> u256 {
            let world = self.world_default();
            let balance: Gold = world.read_model(account);
            balance.amount
        }
    }

    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
            self.world(@"my_game")
        }
    }
}
```

### ERC721-like NFT

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Weapon {
    #[key]
    pub token_id: u256,
    pub owner: ContractAddress,
    pub damage: u32,
    pub rarity: u8,
}

#[starknet::interface]
trait IWeaponNFT<T> {
    fn mint(ref self: T, to: ContractAddress, damage: u32) -> u256;
    fn transfer(ref self: T, to: ContractAddress, token_id: u256);
    fn owner_of(self: @T, token_id: u256) -> ContractAddress;
}

#[dojo::contract]
mod weapon_nft {
    use super::{IWeaponNFT, Weapon};
    use starknet::{ContractAddress, get_caller_address};
    use dojo::model::ModelStorage;

    #[abi(embed_v0)]
    impl WeaponNFTImpl of IWeaponNFT<ContractState> {
        fn mint(ref self: ContractState, to: ContractAddress, damage: u32) -> u256 {
            let mut world = self.world_default();

            let token_id: u256 = world.uuid().into();

            let weapon = Weapon {
                token_id,
                owner: to,
                damage,
                rarity: 1,
            };

            world.write_model(@weapon);
            token_id
        }

        fn transfer(ref self: ContractState, to: ContractAddress, token_id: u256) {
            let mut world = self.world_default();
            let from = get_caller_address();

            let mut weapon: Weapon = world.read_model(token_id);
            assert(weapon.owner == from, 'not owner');

            weapon.owner = to;
            world.write_model(@weapon);
        }

        fn owner_of(self: @ContractState, token_id: u256) -> ContractAddress {
            let world = self.world_default();
            let weapon: Weapon = world.read_model(token_id);
            weapon.owner
        }
    }

    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
            self.world(@"my_game")
        }
    }
}
```

## Token Events

Emit events so Torii and clients can track token operations:

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::event]
pub struct TokenTransferred {
    #[key]
    pub from: ContractAddress,
    #[key]
    pub to: ContractAddress,
    pub amount: u256,
}

// Emit in your functions
world.emit_event(@TokenTransferred { from, to, amount });
```

## Deploying Token Contracts

Token contracts are deployed as **external contracts** alongside your Dojo world.
See `dojo-deploy` skill for general deployment workflow.

### Add to Scarb.toml

```toml
[[target.starknet-contract]]
build-external-contracts = [
    "dojo::world::world_contract::world",
    "tokens::models::m_ERC20Token"
]
```

### Configure in Profile

In `dojo_dev.toml`, define the token as an external contract:

```toml
[[external_contracts]]
contract_name = "ERC20Token"
instance_name = "GoldToken"
salt = "1"
constructor_data = [
    "str:Gold Coin",                # Token name
    "sstr:GOLD",                    # Symbol
    "u256:1000000000000000000",     # Total supply (1e18)
    "0x1234567890abcdef..."         # Owner address
]
```

Add more `[[external_contracts]]` blocks for additional tokens.
Deploy with `sozo build && sozo migrate`.
Note the contract addresses from the output — you need them for Torii.

## Indexing Tokens with Torii

Torii indexes ERC token contracts separately from Dojo world state.
You must explicitly tell Torii which contracts to watch.
See `dojo-indexer` skill for general Torii configuration.

### Configuration

Add token contracts to `[indexing]` using the `ERC20:` or `ERC721:` prefix:

```toml
# torii.toml
[indexing]
contracts = [
    "ERC20:0xYOUR_GOLD_TOKEN_ADDRESS",
    "ERC721:0xYOUR_WEAPON_NFT_ADDRESS",
]
```

Or via CLI:

```bash
torii --world 0xYOUR_WORLD \
  --indexing.contracts "ERC20:0xGOLD_TOKEN" \
  --indexing.contracts "ERC721:0xWEAPON_NFT"
```

You can also index well-known tokens on the network:

```toml
[indexing]
contracts = [
    "ERC20:0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7", # ETH
    "ERC20:0x4718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d", # STRK
]
```

## Querying Token Data

Once indexed, three database tables become available:
- **`tokens`** — metadata (name, symbol, decimals)
- **`balances`** — per-account balances
- **`erc_transfers`** — transfer history

### SQL

```sql
SELECT * FROM tokens;
SELECT * FROM balances WHERE account_address = '0xPLAYER';
SELECT * FROM erc_transfers ORDER BY rowid DESC LIMIT 20;
```

### JavaScript SDK

```typescript
import { useTokens } from "@dojoengine/sdk/react";

function TokenBalance({ address }: { address: string }) {
    const { tokens, getBalance, toDecimal } = useTokens({
        accountAddresses: [address],
    });

    return (
        <div>
            {tokens.map((token, idx) => (
                <div key={idx}>
                    {token.symbol}: {toDecimal(token, getBalance(token))}
                </div>
            ))}
        </div>
    );
}
```

## Troubleshooting

### "Empty tokens/balances tables"
- Verify the contract address matches what was deployed
- Check the prefix is correct (`ERC20:` vs `ERC721:`)
- Ensure the contract implements standard ERC Transfer events

### "Token not showing in Torii"
- Restart Torii after adding new contracts
- Check Torii logs for indexing errors

### "Balance shows 0"
- Tokens are indexed from transfer events, not storage reads
- Mint or transfer tokens to generate events Torii can index

## Related Skills

- **dojo-model**: Token models extend Dojo models
- **dojo-system**: Token logic in systems
- **dojo-test**: Test token operations
- **dojo-deploy**: General world deployment workflow
- **dojo-indexer**: Full Torii configuration and queries
- **dojo-client**: Client SDK integration
