---
name: icons
description: Icon usage conventions and semantic mappings. Use when adding, modifying, or choosing icons.
---

# Icon Standards

## Libraries
- **Radix** (`@radix-ui/react-icons`): UI primitives (dropdowns, modals, tables)
- **react-icons**: Domain icons (status, features)

## Standard Icons

| Concept | Icon | Import |
|---------|------|--------|
| Error | `MdError` | `react-icons/md` |
| Warning | `IoWarningOutline` | `react-icons/io5` |
| Success | `GrStatusGood` | `react-icons/gr` |
| Info | `FaRegLightbulb` | `react-icons/fa` |
| Help | `BsQuestionCircle` | `react-icons/bs` |
| Close | `Cross2Icon` | `@radix-ui/react-icons` |
| Search | `FiSearch` | `react-icons/fi` |
| External link | `ExternalLinkIcon` | `@radix-ui/react-icons` |
| Settings | `GearIcon` | `@radix-ui/react-icons` |
| Copy | `LuCopy` | `react-icons/lu` |
| Trash | `TrashIcon` | `@radix-ui/react-icons` |
| Chevrons | `ChevronDownIcon` etc | `@radix-ui/react-icons` |
| Arrows | `ArrowDownIcon` etc | `@radix-ui/react-icons` |
| Filter | `GoFilter` | `react-icons/go` |
| Star | `GoStar` / `GoStarFill` | `react-icons/go` |
| User | `LuUser` | `react-icons/lu` |
| Reload | `ReloadIcon` | `@radix-ui/react-icons` |

## Domain Icons

| Concept | Icon | Import |
|---------|------|--------|
| Supply | `BsArrowUpCircle` | `react-icons/bs` |
| Deposit | `BsArrowUpCircle` | `react-icons/bs` |
| Borrow | `BsArrowDownLeftCircle` | `react-icons/bs` |
| Repay | `BsArrowUpRightCircle` | `react-icons/bs` |
| Withdraw | `BsArrowDownCircle` | `react-icons/bs` |
| Swap | `LuArrowRightLeft` | `react-icons/lu` |
| History | `GoHistory` | `react-icons/go` |
| Rewards | `FiGift` | `react-icons/fi` |
| Fire | `HiFire` | `react-icons/hi2` |
| Morpho | `PiButterflyDuotone` | `react-icons/pi` |

## Custom Components

| Component | Path |
|-----------|------|
| `SpinnerIcon` | `@/components/icons/SpinnerIcon` |
| `RefetchIcon` | `@/components/ui/refetch-icon` |
| `TokenIcon` | `@/components/shared/token-icon` |
| `NetworkIcon` | `@/components/shared/network-icon` |

## Rules
1. Use standard icon for each concept (no alternatives)
2. Size: `16-18px` inline, `20-24px` standalone
3. Check this doc before adding new icons
