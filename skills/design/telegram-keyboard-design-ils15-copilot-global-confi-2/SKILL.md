---
name: telegram-keyboard-design
description: Design Telegram bot keyboards, buttons, and conversational flows with proper UX patterns. Includes inline keyboards, reply keyboards, button callbacks, and progressive disclosure for better mobile UX.
---

# Telegram Keyboard Design Skill

## When to Use

Use this skill when:
- Designing Telegram bot menus and navigation
- Creating inline buttons for product browsing
- Building conversational flows with progressive disclosure
- Implementing callback handlers for button interactions
- Designing mobile-first keyboard layouts
- Managing state in bot conversations
- Creating rich interaction patterns

## Design Principles

### 1. Progressive Disclosure
Only show relevant buttons at each step, reducing cognitive load:
```
Bad: Show 20 buttons at once
Good: Show 3-5 buttons, then reveal more based on choice
```

### 2. Mobile-First Design
- Buttons are small touch targets
- Stack vertically when possible (2-column max)
- Avoid too many rows (5 max per screen)

### 3. Consistent Navigation
- Always include a "Back" button for multi-step flows
- "Main Menu" to return home
- Clear CTA buttons

## Code Patterns

### 1. Reply Keyboard (Main Menu)

```python
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """Main menu with 2-column layout"""
    keyboard = [
        [
            KeyboardButton("🛍️ Buscar Ofertas"),
            KeyboardButton("💰 Meus Cupons")
        ],
        [
            KeyboardButton("❓ Ajuda"),
            KeyboardButton("⚙️ Configurações")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,      # Auto-size buttons
        one_time_keyboard=False    # Keep keyboard visible
    )
```

### 2. Inline Keyboard (Button Actions)

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_product_keyboard(product_id: int, page: int = 1):
    """Product view with action buttons"""
    keyboard = [
        [
            InlineKeyboardButton("📋 Detalhes", callback_data=f"product_details_{product_id}"),
            InlineKeyboardButton("🔗 Link", url=f"https://ofertachina.com/p/{product_id}")
        ],
        [
            InlineKeyboardButton("❤️ Salvar", callback_data=f"save_product_{product_id}"),
            InlineKeyboardButton("📤 Compartilhar", callback_data=f"share_product_{product_id}")
        ],
        [
            InlineKeyboardButton("⬅️ Voltar", callback_data="back_to_products")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_pagination_keyboard(page: int, total_pages: int):
    """Pagination buttons"""
    keyboard = []
    
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"page_{page-1}"))
    
    buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
    
    if page < total_pages:
        buttons.append(InlineKeyboardButton("Próxima ➡️", callback_data=f"page_{page+1}"))
    
    keyboard.append(buttons)
    return InlineKeyboardMarkup(keyboard)
```

### 3. Category Selection Flow

```python
# Progressive disclosure: First show categories, then products

def get_category_keyboard():
    """First step: Choose category"""
    keyboard = [
        [InlineKeyboardButton("🖥️ Eletrônicos", callback_data="cat_electronics")],
        [InlineKeyboardButton("👗 Moda", callback_data="cat_fashion")],
        [InlineKeyboardButton("🏠 Casa", callback_data="cat_home")],
        [InlineKeyboardButton("🎮 Games", callback_data="cat_games")],
        [InlineKeyboardButton("📚 Livros", callback_data="cat_books")],
        [InlineKeyboardButton("🔄 Voltar", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_subcategory_keyboard(category: str):
    """Second step: Choose subcategory within category"""
    subcategories = {
        "electronics": [
            ("📱 Smartphones", "subcat_phones"),
            ("💻 Laptops", "subcat_laptops"),
            ("⌚ Wearables", "subcat_wearables"),
        ],
        "fashion": [
            ("👔 Homem", "subcat_mens"),
            ("👗 Mulher", "subcat_womens"),
            ("👶 Infantil", "subcat_kids"),
        ]
    }
    
    keyboard = []
    for label, callback in subcategories.get(category, []):
        keyboard.append([InlineKeyboardButton(label, callback_data=callback)])
    
    keyboard.append([InlineKeyboardButton("⬅️ Voltar", callback_data="categories")])
    
    return InlineKeyboardMarkup(keyboard)
```

### 4. Callback Handler

```python
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def handle_product_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()  # Remove loading spinner
    
    callback_data = query.data
    
    if callback_data.startswith("product_details_"):
        product_id = int(callback_data.split("_")[-1])
        await show_product_details(query, product_id, context)
    
    elif callback_data.startswith("save_product_"):
        product_id = int(callback_data.split("_")[-1])
        await save_to_favorites(query, product_id, context)
    
    elif callback_data.startswith("page_"):
        page = int(callback_data.split("_")[-1])
        await show_page(query, page, context)
    
    elif callback_data == "main_menu":
        await query.edit_message_text(
            text="🏠 Menu Principal",
            reply_markup=get_main_keyboard()
        )

async def show_product_details(query, product_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed product view"""
    # Fetch product from database
    product = await get_product(product_id)
    
    text = f"""
📦 *{product['title']}*

💰 Preço: R$ {product['price']:.2f}
⭐ Avaliação: {product['rating']}/5
📦 Envio: Frete grátis

{product['description']}

🔗 [Ver na loja]({product['url']})
    """.strip()
    
    await query.edit_message_text(
        text=text,
        reply_markup=get_product_keyboard(product_id),
        parse_mode="Markdown"
    )

async def save_to_favorites(query, product_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Toggle favorite status"""
    user_id = query.from_user.id
    
    # Save to database
    saved = await toggle_favorite(user_id, product_id)
    
    status = "✅ Salvo!" if saved else "❌ Removido"
    await query.answer(status, show_alert=False)
```

### 5. Search with Buttons

```python
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search input"""
    search_query = update.message.text
    
    # Search products
    products = await search_products(search_query)
    
    if not products:
        await update.message.reply_text("❌ Nenhum produto encontrado")
        return
    
    # Show first 5 products with next page button
    text = "🔍 Resultados da busca:\n\n"
    
    keyboard = []
    for i, product in enumerate(products[:5], 1):
        text += f"{i}. {product['title']}\n💰 R$ {product['price']}\n\n"
        
        keyboard.append([
            InlineKeyboardButton(
                f"#{i} Ver",
                callback_data=f"product_details_{product['id']}"
            )
        ])
    
    # Pagination if more results
    if len(products) > 5:
        keyboard.append([
            InlineKeyboardButton("Próxima página ➡️", callback_data="search_next_page")
        ])
    
    keyboard.append([InlineKeyboardButton("🔄 Nova busca", callback_data="main_menu")])
    
    await update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
```

### 6. Confirmation Dialog

```python
def get_confirm_keyboard(action_id: str):
    """Confirmation buttons"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirmar", callback_data=f"confirm_{action_id}"),
            InlineKeyboardButton("❌ Cancelar", callback_data="cancel")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

async def handle_share(query, product_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Share product confirmation"""
    product = await get_product(product_id)
    
    text = f"""
Compartilhar este produto?

📦 {product['title']}
💰 R$ {product['price']}
    """.strip()
    
    await query.edit_message_text(
        text=text,
        reply_markup=get_confirm_keyboard(f"share_{product_id}")
    )
```

## Mobile UX Checklist

✅ Buttons are **30-40px** tall (easy to tap)  
✅ Max **2 buttons per row** horizontally  
✅ Max **5 rows** visible without scrolling  
✅ **Back buttons** always available  
✅ **Loading state** with `query.answer()`  
✅ **Edit, not reply** for follow-up messages  
✅ **Emoji** for visual clarity  
✅ **Short labels** (max 20 chars)  

## Anti-Patterns ❌

❌ Show 20 buttons at once  
❌ Nested buttons without back  
❌ Tiny buttons (<25px)  
❌ No loading feedback (frozen UI)  
❌ Same text with different actions  
❌ Deep button hierarchies (>3 levels)  

## Related Files

- [keyboard-templates.py](./keyboard-templates.py) - Ready-to-use keyboard builders
- [callback-handlers.py](./callback-handlers.py) - Callback handler examples
- [flow-patterns.md](./flow-patterns.md) - Common conversation flows

## References

- python-telegram-bot: https://python-telegram-bot.readthedocs.io/
- Telegram Bot API: https://core.telegram.org/bots/api#inlinekeyboardmarkup
- UX Best Practices: https://core.telegram.org/bots/design
