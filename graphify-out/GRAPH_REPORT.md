# Graph Report - besporman-tg-bot  (2026-10-03)

## Corpus Check
- Corpus is ~8,166 words - fits in a single context window. You may not need a graph.

## Summary
- 252 nodes · 559 edges · 15 communities (14 shown, 1 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 89 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Subsystem 0
- Subsystem 1
- Admin & Management Services
- Admin & Management Services
- Showcase & Portfolios
- Admin & Management Services
- Admin & Management Services
- Admin & Management Services
- Subsystem 8
- Subsystem 9
- Subsystem 10
- Subsystem 11
- Subsystem 12

## God Nodes (most connected - your core abstractions)
1. `User` - 14 edges
2. `Order` - 14 edges
3. `handle_order_description()` - 14 edges
4. `OrderStatus` - 13 edges
5. `Base` - 11 edges
6. `handle_support_message()` - 11 edges
7. `save_message()` - 11 edges
8. `Portfolio` - 10 edges
9. `handle_admin_bridge_send()` - 10 edges
10. `handle_client_bridge_answer()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_order_submission_flow()` --uses--> `OrderStatus`  [INFERRED]
  tests/test_router_integration.py → src/besporman_tg_bot/db/models.py
- `test_order_message_persistence()` --uses--> `SenderType`  [INFERRED]
  tests/test_order_fsm.py → src/besporman_tg_bot/db/models.py
- `test_order_message_persistence()` --calls--> `save_message()`  [INFERRED]
  tests/test_order_fsm.py → src/besporman_tg_bot/services/message_service.py
- `test_order_message_persistence()` --calls--> `get_order_messages()`  [INFERRED]
  tests/test_order_fsm.py → src/besporman_tg_bot/services/message_service.py
- `test_order_submission_flow()` --calls--> `get_orders_by_status()`  [INFERRED]
  tests/test_router_integration.py → src/besporman_tg_bot/services/order_service.py

## Import Cycles
- None detected.

## Communities (15 total, 1 thin omitted)

### Community 0 - "Subsystem 0"
Cohesion: 0.11
Nodes (35): ReplyKeyboardMarkup, SenderType, handle_cancel(), handle_nav_main_menu(), handle_start(), callback_query, CallbackQuery, FSMContext (+27 more)

### Community 1 - "Subsystem 1"
Cohesion: 0.08
Nodes (25): Dispatcher, listens_for, create_bot(), create_dispatcher(), Bot, get_db_session(), init_db(), AsyncSession (+17 more)

### Community 2 - "Admin & Management Services"
Cohesion: 0.12
Nodes (28): DeclarativeBase, Base, AdminAuditLog, Portfolio, PortfolioMedia, Testimonial, AsyncSession, seed_initial_data() (+20 more)

### Community 3 - "Admin & Management Services"
Cohesion: 0.18
Nodes (29): Order, OrderStatus, User, handle_admin_audit_logs(), handle_admin_dashboard(), handle_admin_order_list(), handle_admin_stats(), handle_return_dashboard() (+21 more)

### Community 4 - "Showcase & Portfolios"
Cohesion: 0.15
Nodes (22): handle_portfolio_detail(), handle_portfolio_list_callback(), handle_portfolio_menu(), AsyncSession, callback_query, CallbackQuery, message, handle_services() (+14 more)

### Community 5 - "Admin & Management Services"
Cohesion: 0.18
Nodes (20): Message, handle_admin_ask_click(), handle_admin_bridge_send(), handle_admin_cancel(), handle_admin_reply_click(), handle_client_bridge_answer(), AsyncSession, Bot (+12 more)

### Community 6 - "Admin & Management Services"
Cohesion: 0.36
Nodes (9): handle_set_status(), handle_status_menu(), handle_view_order(), AsyncSession, callback_query, CallbackQuery, get_admin_order_actions_keyboard(), get_admin_status_selection_keyboard() (+1 more)

### Community 7 - "Admin & Management Services"
Cohesion: 0.29
Nodes (7): Filter, IsAdminFilter, CallbackQuery, asyncio, test_admin_filter_authorized_ids(), test_admin_filter_none_user(), test_admin_filter_unauthorized_ids()

### Community 8 - "Subsystem 8"
Cohesion: 0.36
Nodes (7): parametrize, is_profane(), normalize_persian_text(), _strip_persian_suffixes(), test_normalization_removes_repeated_chars_and_diacritics(), test_profanity_filter_blocked_texts(), test_profanity_filter_clean_texts()

### Community 9 - "Subsystem 9"
Cohesion: 0.33
Nodes (7): Path, contains_zwnj(), main(), sanitize_zwnj(), scan_directory_for_zwnj(), test_zero_zwnj_across_entire_project(), test_zwnj_sanitizer_utility()

### Community 10 - "Subsystem 10"
Cohesion: 0.36
Nodes (7): handle_resume_dev1(), handle_resume_dev2(), handle_team_overview(), callback_query, CallbackQuery, message, get_team_keyboard()

### Community 11 - "Subsystem 11"
Cohesion: 0.47
Nodes (4): Connection, do_run_migrations(), run_async_migrations(), run_migrations_online()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Portfolio` connect `Admin & Management Services` to `Showcase & Portfolios`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `User` connect `Admin & Management Services` to `Subsystem 0`, `Admin & Management Services`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `Base` connect `Admin & Management Services` to `Subsystem 1`, `Admin & Management Services`, `Admin & Management Services`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `User` (e.g. with `handle_admin_dashboard()` and `handle_admin_stats()`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Order` (e.g. with `handle_admin_dashboard()` and `handle_admin_stats()`) actually correct?**
  _`Order` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `handle_order_description()` (e.g. with `SenderType` and `User`) actually correct?**
  _`handle_order_description()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `OrderStatus` (e.g. with `handle_admin_dashboard()` and `handle_admin_order_list()`) actually correct?**
  _`OrderStatus` has 9 INFERRED edges - model-reasoned connections that need verification._