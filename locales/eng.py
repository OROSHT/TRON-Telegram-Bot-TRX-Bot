# Global
gl_next = "▶️ Next"
gl_back = "◀️ Back"
gl_yes = "✅ Yes"
gl_yep = "✅ yep"
gl_no = "❌ No"
gl_cancel = "❌ Cancel"
gl_refresh = "🔄 Refresh"
gl_delete = "🗑️ Delete"
gl_edit = "✏️ Edit"
gl_configure = "⚙️ Configure"
gl_pcs = "pcs."
gl_last_update = "Last update"


# Main menu
mm_global = "⚙️ Global switches"
mm_notifications = "🔔 Notification settings"
mm_autoresponse = "🤖 Autoresponse settings"
mm_autodelivery = "📦 Auto-delivery settings"
mm_blacklist = "🚫 Blacklist settings"
mm_templates = "📝 Answer templates"
mm_greetings = "👋 Greeting message"
mm_order_confirm = "✅ Order confirmation response"
mm_review_reply = "⭐ Response to reviews"
mm_new_msg_view = "✉️ Appearance of new msg. notification"
mm_plugins = "🧩 Plugins"
mm_configs = "📁 Configs"

# Global switches
gs_autoraise = "{} Auto-raise"
gs_autoresponse = "{} Autoresponse"
gs_autodelivery = "{} Auto-delivery"
gs_nultidelivery = "{} Multi-delivery"
gs_autorestore = "{} Reactivate lots"
gs_autodisable = "{} Deactivate lots"
gs_old_msg_mode = "{} Old Message Receiving Mode"

# Notification settings
ns_new_msg = "{} New message"
ns_cmd = "{} Command received"
ns_new_order = "{} New order"
ns_order_confirmed = "{} Order confirmed"
ns_lot_activate = "{} Lot reactivated"
ns_lot_deactivate = "{} Lot deactivated"
ns_delivery = "{} Goods delivered"
ns_raise = "{} Lots raised"
ns_new_review = "{} New review"
ns_bot_start = "{} Bot start"
ns_other = "{} Other (plugins)"

# Autoresponse settings
ar_edit_commands = "✏️ Edit existing commands"
ar_add_command = "➕ Add command / set of commands"
ar_to_ar = "🤖 Back to autoresponse settings"
ar_to_mm = "📋 Back to main menu"
ar_edit_response = "✏️ Edit response"
ar_edit_notification = "✏️ Edit notification text"
ar_notification = "{} Telegram notification"
ar_add_more = "➕ Add more"
ar_add_another = "➕ Add another"

# Auto-delivery settings
ad_edit_autodelivery = "🗳️ Edit lots auto-delivery"
ad_add_autodelivery = "➕ Link auto-delivery to lot"
ad_add_another_ad = "➕ Link another"
ad_add_more_ad = "➕ Link more"
ad_edit_goods_file = "📋 Edit goods files"
ad_upload_goods_file = "⤴️ Upload goods file"
ad_create_goods_file = "➕ Create goods file"
ad_to_ad = "📦 Back to auto-delivery settings"
ad_to_mm = "📋 Back to main menu"

# - Edit auto-delivery
ea_edit_delivery_text = "✏️ Edit delivery text"
ea_link_goods_file = "⛓️ Link goods file"
ea_delivery = "{} Auto-delivery"
ea_multidelivery = "{} Multi-delivery"
ea_restore = "{} Reactivation"
ea_deactivate = "{} Deactivation"
ea_test = "🗝️ Auto-delivery key"
ea_more_test = "🗝️ 1 more key"
ea_link_another_gf = "⛓️ Another file"

# - Add auto-delivery
fl_manual = "➕ Enter manually"

# - Goods files
gf_add_goods = "➕ Add goods"
gf_download = "⤵️ Download"
gf_create_another = "➕ Create another"
gf_create_more = "➕ Create more"
gf_add_more = "➕ Add more"
gf_try_add_again = "➕ Try again"

# Blacklist settings
bl_autodelivery = "{} Don't deliver goods"
bl_autoresponse = "{} Don't respond to commands"
bl_new_msg_notifications = "{} Don't notify about new messages"
bl_new_order_notifications = "{} Don't notify about new orders"
bl_command_notifications = "{} Don't notify about commands received"

# Answer templates
tmplt_add = "➕ Add template"
tmplt_add_more = "➕ Add more"
tmplt_add_another = "➕ Add another"

# Greeting settings
gr_greetings = "{} Greet users"
gr_cache_init_chats = "{} Ignore existing chats"
gr_ignore_sys_msgs = "{} Ignore system messages"
gr_edit_message = "✏️ Change the text of the welcome message"

# Order confirmation response settings
oc_send_reply = "{} Send message"
oc_edit_message = "✏️ Change the text of the message"

# Appearance of new msg. notification
mv_incl_my_msg = "{} Show my messages"
mv_incl_fp_msg = "{} Show FunPay messages"
mv_incl_bot_msg = "{} Show bot messages"
mv_only_my_msg = "{} Notify, if only my messages"
mv_only_fp_msg = "{} Notify, if only FunPay messages"
mv_only_bot_msg = "{} Notify, if only bot messages"

# Configs
cfg_download_main = "⤵️ Download main config"
cfg_download_ar = "⤵️ Download autoresponse config"
cfg_download_ad = "⤵️ Download auto-delivery config"
cfg_upload_main = "⤴️ Upload main config"
cfg_upload_ar = "⤴️ Upload autoresponse config"
cfg_upload_ad = "⤴️ Upload auto-delivery config"


# New order
ord_refund = "💸 Make a refund"
ord_open = "🌐 Open order page"
ord_answer = "📨 Answer"
ord_templates = "📝 Templates"


# New message
msg_reply = "📨 Reply"
msg_reply2 = "📨 Reply"
msg_templates = "📝 Templates"
msg_more = "➕ More"


# Messages texts
access_denied = "👋 Hi, <b><i>{}</i></b>!\n\n❌ You are an unauthorized user.\n\n"\
                "🔑 Send me the <u><b>secret key</b></u> you entered during the initial setup to "\
                "gain access to the control panel."

access_granted = "🔓 Access granted!\n\n"\
                 "🔕 Keep in mind that I <b><u>don't send any notifications to this chat</u></b>.\n\n"\
                 "🔔 You can set up notifications for <b><u>this chat</u></b> in the settings menu.\n\n"\
                 "⚙️ To open the <i>FunPay Vertex</i> settings menu, send me /menu."

param_disabled = "❌ This parameter is disabled globally and cannot be changed for this lot.\n\n"\
                 "❔ Switching global parameters is available in the global switch menu "\
                 "(/menu -> ⚙️ Global switches)."

old_mode_help = """<b>New Message Receiving Mode</b>
✅ <i>FPV</i> gets the full chat history and sees all data about all new messages.
✅ <i>FPV</i> can see images in chat and forward them to <i>Telegram</i> chat.
✅ <i>FPV</i> can determine exactly who wrote, whether it was you, your interlocutor, or a 3rd party (arbitrator).
❌ Because <i>FPV</i> gets the full chat history to detect new messages, the chat becomes "read" (not lit orange).

<b>Old Message Receiving Mode</b>
✅ Chats that you have not personally read remain unread (lit orange).
✅ Works a little bit faster than the new mode.
❌ <i>FPV</i> doesn't get the full chat history, so it sees only the last message. If the user quickly writes several messages, <i>FPV</i> will see only the last one.
❌ <i>FPV</i> cannot see images in chat and forward them to <i>Telegram</i> chat.
❌ <i>FPV</i> cannot determine exactly who wrote: you or the person you are chatting with. If the chat is not read, then the message is from the interlocutor, otherwise it is from you. However, if you are viewing the chat when you receive messages, this logic can sometimes fail. Also, <i>FPV</i> will not be able to determine if a 3rd party (arbitrator) wrote into the chat.

❗ If you click the <code>More</code> button in a new message notification, <i>FPV</i> will "read" the chat and show the last 15 messages, including images. <i>FPV</i> will also be able to determine who the author of the messages is."""

bot_started = """✅ Telegram bot is running!\n
✅ You can <b><u>customize configurations</u></b> and <b><u>make full use of the <i>Telegram</i> bot's functionality.</u></b>.\n
❌ <i>FunPay Vertex</i> is not initialized yet and none of its functions work.\n
🔃 As soon as <i>FunPay Vertex</i> is initialized, this message will change.\n
📋 If <i>FPV</i> does not initialize for a long time, check the logs with /logs"""

fpv_init = """✅ <b><u>FunPay Vertex initialized!</u></b>\n
ℹ️ <b><i>Version:</i></b> <code>{}</code>
👑 <b><i>Account:</i></b>  <code>{}</code> | <code>{}</code>
💰 <b><i>Balance:</i></b> <code>{}₽, {}$, {}€</code>
📊 <b><i>Active orders:</i></b>  <code>{}</code>"""

create_test_ad_key = "Enter the name of the lot whose auto-delivery you want to test."

test_ad_key_created = """✅ A one-time key for <code>{}</code> delivery has been created.\n
Send the command from below to chat with the user to whom you want to deliver the item.\n
<code>!автовыдача {}</code>"""

about = """<b>🐺 FunPay Vertex 🐺 v{}</b>\n
<i>Telegram chat:</i> @funpayplace
<i>Developer:</i> NightStranger, Lemarty"""

sys_info = """<b><u>Data summary</u></b>

<b>CPU:</b>
{}
    Used by <i>FPV</i>: <code>{}%</code>

<b>RAM:</b>
    Total:  <code>{} MB</code>
    Used:  <code>{} MB</code>
    Free:  <code>{} MB</code>
    Used by <i>FPV</i>:  <code>{} MB</code>

<b>Other:</b>
    Uptime:  <code>{}</code>
    Chat ID:  <code>{}</code>"""

act_blacklist = """Enter the username you want to add to the blacklist."""
already_blacklisted = "❌ <code>{}</code> is already on the blacklist."
user_blacklisted = "✅ <code>{}</code> is blacklisted."
act_unban = "Enter the username you want to remove from the blacklist."
not_blacklisted = "❌ <code>{}</code> is not blacklisted."
user_unbanned = "✅ <code>{}</code> is no longer blacklisted."
blacklist_empty = "❌ Blacklist is empty."

act_edit_watermark = "Enter a new watermark text. If you want to remove the watermark, send <code>-</code>."
watermark_changed = "✅ The message watermark has been changed."
watermark_deleted = "✅ The message watermark has been deleted."
watermark_error = "❌ Invalid watermark."

logfile_not_found = "❌ Log file not found."
logfile_sending = "Sending log file (it may take some time)..."
logfile_error = "❌ Failed to send log file."
logfile_deleted = "🗑️ Deleted {} logfile(s)."

update_no_tags = "❌ Failed to get the version list. Try again later."
update_lasted = "✅ You have the latest version FunPayVertex {}"
update_get_error = "❌ Failed to get new version information. Try again later."
update_available = "<b><u>New version available!</u></b>\n\n\n{}\n\n{}"
update_update = "To update, enter the command /update"
update_backup_created = "✅ Backed up configs and storage in <code>backup.zip</code>."
update_backup_error = "❌ Failed to back up configs and storage."
update_downloaded = "✅ The update is downloaded. Installing ..."
update_download_error = "❌ An error occurred while downloading the update."
update_done = "✅ The update is installed! Restart the FPV with the /restart command."
update_done_exe = "✅ The update is installed! New <code>FPV.exe</code> is in <code>update</code> folder. "\
                  "Turn off <i>FPV</i>, replace old <code>FPV.exe</code> with new one and run <code>Start.bat</code>. "
update_install_error = "❌ An error occurred while installing the update."

restarting = "Restarting..."
power_off_0 = """<b><u>Are you sure you want to turn me off?</u></b>\n
You <b><u>wont be able</u></b> to turn me on via <i>Telegram</i>!"""
power_off_1 = "I'll ask again, just in case.\n\n<b><u>Are you sure about this?</u></b>"
power_off_2 = """Just for the record:
you have to go to the server or go to your computer (or wherever you have me) and run me manually!"""
power_off_3 = "Not that I'm imposing, but if you want to apply changes to the main config, " \
              "you can just restart me with the /restart command."
power_off_4 = "Do you even read my messages? Let's put you to the test: yes = no, no = yes."\
              "I'm sure you don't even read my messages, but I write important info here."
power_off_5 = "Hell yeah?.."
power_off_6 = "Okay, okay, I'm off..."
power_off_cancelled = "The shutdown has been cancelled."
power_off_error = "❌ This button does not belong to this session.\nCall this menu again."

enter_msg_text = "Enter message text."
msg_sent = "✅ Message sent to <a href=\"https://funpay.com/chat/?node={}\">{}</a> chat."
msg_sending_error = "❌ Failed to send a message to <a href=\"https://funpay.com/chat/?node={}\">{}</a> chat."
send_img = "Send me an image."

greeting_changed = "✅ The greeting text has been changed."
order_confirm_changed = "✅ The text of the order confirmation reply has been changed!"
review_reply_changed = "✅ The text of {} review reply has been changed!"
review_reply_empty = "❌ {} review reply text not set."
review_reply_text = "{} review reply text:\n<code>{}</code>"

get_chat_error = "❌ Failed to get chat data."
viewing = "Viewing"
you = "You"
support = "support"
photo = "Photo"

refund_attempt = "❌ Failed to refund order <code>#{}</code>.\n<code>{}</code> attempts left."
refund_error = "❌ Failed to refund order <code>#{}</code>."
refund_complete = "✅ The #{} order has been refunded."

updating_profile = "Updating account statistics (this may take some time)..."
profile_updating_error = "❌ Failed to update account statistics."

ad_lot_not_found_err = "❌ Lot with index <code>{}</code> not found."
ad_already_ad_err = "❌ Lot <code>{}</code> is already set up for auto-delivery."
ad_lot_already_exists = "❌ The lot <code>{}</code> already has auto-delivery linked to it."
ad_lot_linked = "✅ Auto-delivery linked to lot <code>{}</code>."
ad_link_gf = "Enter the goods file name.\nSend <code>-</code>, if you want to unlink the goods file.\n\n"\
             "If the goods file does not exist, it will be created automatically."
ad_gf_unlinked = "✅ Goods file successfully unlinked from <code>{}</code>."
ad_gf_linked = "✅ The goods file <code>storage/products/{}</code> linked to <code>{}</code>."
ad_gf_created_and_linked = "✅ The goods file <code>storage/products/{}</code> <b><u>created</u></b> and linked to <code>{}</code>."
ad_creating_gf = "🔄 Creating goods file <code>storage/products/{}</code>..."
ad_product_var_err = "❌ There is the goods file linked to <code>{}</code>, but there is no <code>$product</code> variable in the delivery text."
ad_product_var_err2 = "❌ Can't link the goods file, because the <code>$product</code> variable is missing from the delivery text."
ad_text_changed = "✅ The delivery text of <code>{}</code> has been changed to <code>{}</code>."
ad_updating_lots_list = "Updating lots and categories data (it may take some time)..."
ad_lots_list_updating_err = "❌ Failed to update lots and categories data."
gf_not_found_err = "❌ Goods file with index <code>{}</code> not found."
copy_lot_name = "Send the name of the lot exactly as on FunPay."

act_create_gf = "Enter the name of the new goods file."
gf_name_invalid = "❌ Invalid file name.\n\n" \
                  "Only <b><u>English</u></b> and <b><u>Russian</u></b> characters are allowed in the name,"\
                  "as well as <code>_</code>, <code>-</code> and <code>space</code>."
gf_already_exists_err = "❌ Goods file <code>{}</code> already exists."
gf_creation_err = "❌ An error occurred while creating the <code>{}</code> file."
gf_created = "✅ Goods file <code>storage/products/{}</code> created."
gf_amount = "Goods amount"
gf_uses = "Used in lots"
gf_send_new_goods = "Enter the goods you want to add to goods file.\n\nEach new line (<code>Shift+Enter</code>) is a new item."
gf_add_goods_err = "❌ Failed to add new goods."
gf_new_goods = "✅ <code>{}</code> item(s) added to <code>storage/products/{}</code>."
gf_empty_error = "❌ File storage/products/{} is empty."
gf_linked_err = "❌ File <code>storage/products/{}</code> is linked to one ore more lots.\n"\
                "Before deleting this goods file, unlink it from all lots."
gf_deleting_err = "❌ Failed to delete file <code>storage/products/{}</code>."

ar_cmd_not_found_err = "❌ Command with index <code>{}</code> not found."
ar_subcmd_duplicate_err = "❌ The command <code>{}</code> is duplicated in the command net."
ar_cmd_already_exists_err = "❌ The command <code>{}</code> already exists."
ar_enter_new_cmd = "Enter a new command (or several commands via <code>|</code>)."
ar_cmd_added = "Added a new command <code>{}</code>."
ar_response_text = "Response text"
ar_notification_text = "Notification text"
ar_response_text_changed = "✅ The response text of the command <code>{}</code> has been changed to <code>{}</code>."
ar_notification_text_changed = "✅ The notification text of the command <code>{}</code> has been changed to <code>{}</code>"

cfg_main = "Main config."
cfg_ar = "Autoresponse config."
cfg_ad = "Auto-delivery config."
cfg_not_found_err = "❌ Config {} not found."
cfg_empty_err = "❌ Config {} is empty."

tmplt_not_found_err = "❌ Answer template with index <code>{}</code> not found."
tmplt_already_exists_err = "❌ Such a template already exists."
tmplt_added = "✅ Template added."
tmplt_msg_sent = "✅ Message sent to <a href=\"https://funpay.com/chat/?node={}\">{}</a> chat.\n\n<code>{}</code>"

# - Menus desc
desc_main = "Select a settings category."
desc_gs = "Here you can turn the basic <i>FPV</i> functions on and off."
desc_ns = """Here you can configure notifications.\n
<b><u>Settings are separate for each <i>Telegram</i> chat!</u></b>\n
Current chat ID: <code>{}</code>"""
desc_bl = "Here you can set restrictions for blacklisted users."
desc_ar = "Here you can add commands or edit existing ones."
desc_ar_list = "Chose a command / commands set you are interested in."

desc_ad = "Here you can change auto-delivery settings, upload/download goods files, etc."
desc_ad_list = "This is a list of lots that have auto-delivery linked to them. Select the lot you are interested in."
desc_ad_fp_lot_list = "This is a list of lots from your FunPay profile. Select the lot you're interested in to link auto-delivery to it.\n" \
                      "If a lot is missing from the list, click the  <code>🔄 Refresh</code> button.\n\n" \
                      "Last scanning: {}"
desc_gf = "Choose a goods file you are interested in."

desc_mv = "Here you can configure the appearance of new message notifications."
desc_gr = "Here you can configure the welcome message for new users.\n\n<b>Greeting text:</b>\n<code>{}</code>"
desc_oc = "Here you can configure an order confirmation message.\n\n<b>Message text:</b>\n<code>{}</code>"
desc_or = "Here you can configure your response to feedback."
desc_an = "Here you can configure notifications about announcements."
desc_cfg = "Hare you can download and upload configs."
desc_tmplt = "Here you can add and delete answer templates."

# - Commands desc
cmd_menu = "open settings"
cmd_language = "change language"
cmd_profile = "account statistics"
cmd_test_lot = "create one-time delivery key"
cmd_upload_img = "upload an image to FunPay"
cmd_ban = "add user to the blacklist"
cmd_unban = "delete user from blacklist"
cmd_black_list = "blacklist"
cmd_watermark = "change message watermark"
cmd_logs = "download current log-file"
cmd_del_logs = "delete old log-files"
cmd_about = "about current version"
cmd_old_orders = "sends a list of open orders that are more than 24 hours old"
cmd_sys = "system load information"
cmd_keyboard = "open keyboard"
cmd_change_cookie = "change golden_key cookie"
cmd_restart = "restart FPV"
cmd_power_off = "shutdown FPV"


# - Variables desc
v_edit_greeting_text = "Enter the text of the welcome message."
v_edit_order_confirm_text = "Enter the text of the order confirmation response."
v_edit_review_reply_text = "Enter the {} review response text."
v_edit_delivery_text = "Enter a new delivery text."
v_edit_response_text = "Enter a new response text."
v_edit_notification_text = "Enter a new Telegram notification text."
V_new_template = "Enter a text of the new answer template."
v_list = "Variables list"
v_date = "<code>$date</code> - current date in <i>DD.MM.YYYY</i> format."
v_date_text = "<code>$date_text</code> - current date in <i>January 1</i> format."
v_full_date_text = "<code>$full_date_text</code> - current date in <i>January 1, 2020</i> format."
v_time = "<code>$time</code> - current time in <i>HH:MM</i> format."
v_full_time = "<code>$full_time</code> - current time in <i>HH:MM:SS</i> format."
v_photo = "<code>$photo=[PHOTO ID]</code> - photo. Instead of <code>PHOTO ID</code>, "\
          "type the photo ID obtained with the /upload_img command."
v_order_id = "<code>$order_id</code> - order ID (without #)"
v_order_title = "<code>$order_title</code> - order title."
v_product = "<code>$product</code> - item(s) from goods file. xc Works only if goods file linked."
v_chat_id = "<code>$chat_id</code> - chat ID."
v_message_text = "<code>$message_text</code> - interlocutors message text."
v_username = "<code>$username</code> - interlocutors username."


# Exception texts
exc_param_not_found = "The option \"{}\" not found."
exc_param_cant_be_empty = "The value of the option \"{}\" cannot be empty."
exc_param_value_invalid = "Invalid value of the option \"{}\". Possible values: {}. Current value: \"{}\"."
exc_goods_file_not_found = "Specified goods file \"{}\" not found."
exc_goods_file_is_empty = "No items in goods file \"{}\"."
exc_not_enough_items = "Not enough items in goods file \"{}\". Requested: {}, available: {}."
exc_no_product_var = "\"productsFileName\" is specified, but the $product variable is not in \"response\"."
exc_no_section = "Section does not exists."
exc_section_duplicate = "Section duplicate found."
exc_cmd_duplicate = "The command or the subcommand \"{}\" already exists."
exc_cfg_parse_err = "Error in {} config, in the [{}] section: {}"
exc_plugin_field_not_found = "Failed to load the plugin \"{}\": required field \"{}\" does not exists."

# Logs
log_tg_initialized = "$MAGENTATelegram bot initialized."
log_tg_started = "$CYANTelegram bot $YELLOW@{}$CYAN started."
log_tg_handler_error = "An error occurred while executing the Telegram bot handler."
log_tg_update_error = "An error occurred while getting Telegram updates (probably an invalid token?)."
log_tg_notification_error = "An error occurred while sending a notification to chat $YELLOW{}$RESET."
log_access_attempt = "$MAGENTA@{} (ID: {})$RESET tried to access the control panel. I'm holding him back as best I can!"
log_click_attempt = "$MAGENTA@{} (ID: {})$RESET presses the control panel buttons in $MAGENTA@{} (ID: {})$RESET. He won't make it!"
log_access_granted = "$MAGENTA@{} (ID: {})$RESET gained access to the control panel."
log_new_ad_key = "$MAGENTA@{} (ID: {})$RESET created a key to deliver $YELLOW{}$RESET: $CYAN{}$RESET."
log_user_blacklisted = "$MAGENTA@{} (ID: {})$RESET has blacklisted $YELLOW{}$RESET."
log_user_unbanned = "$MAGENTA@{} (ID: {})$RESET has removed $YELLOW{}$RESET from the blacklist."
log_watermark_changed = "$MAGENTA@{} (ID: {})$RESET changed the message watermark to YELLOW{}$RESET."
log_watermark_deleted = "$MAGENTA@{} (ID: {})$RESET deleted the message watermark."
log_greeting_changed = "$MAGENTA@{} (ID: {})$RESET changed the greeting text to $YELLOW{}$RESET."
log_order_confirm_changed = "$MAGENTA@{} (ID: {})$RESET changed the text of order confirmation reply to $YELLOW{}$RESET."
log_review_reply_changed = "$MAGENTA@{} (ID: {})$RESET changed the text of {}-star(s) review reply to $YELLOW{}$RESET."
log_param_changed = "$MAGENTA@{} (ID: {})$RESET changed value of $CYAN{}$RESET in $YELLOW[{}]$RESET section to $YELLOW{}$RESET."
log_notification_switched = "$MAGENTA@{} (ID: {})$RESET switched notifications $YELLOW{}$RESET for chat $YELLOW{}$RESET to $CYAN{}$RESET."
log_ad_linked = "$MAGENTA@{} (ID: {})$RESET linked auto-delivery to lot $YELLOW{}$RESET."
log_ad_text_changed = "$MAGENTA@{} (ID: {})$RESET changed the delivery text of  $YELLOW{}$RESET to $YELLOW\"{}\"$RESET."
log_ad_deleted = "$MAGENTA@{} (ID: {})$RESET deleted auto-delivery from $YELLOW{}$RESET."
log_gf_created = "$MAGENTA@{} (ID: {})$RESET created goods file $YELLOWstorage/products/{}$RESET."
log_gf_unlinked = "$MAGENTA@{} (ID: {})$RESET unlined goods file from $YELLOW{}$RESET."
log_gf_linked = "$MAGENTA@{} (ID: {})$RESET linked goods file $YELLOWstorage/products/{}$RESET to $YELLOW{}$RESET."
log_gf_created_and_linked = "$MAGENTA@{} (ID: {})$RESET created and linked goods file $YELLOWstorage/products/{}$RESET to $YELLOW{}$RESET."
log_gf_new_goods = "$MAGENTA@{} (ID: {})$RESET added $CYAN{}$RESET item(s) in $YELLOWstorage/products/{}$RESET."
log_gf_downloaded = "$MAGENTA@{} (ID: {})$RESET requested the goods file $YELLOWstorage/products/{}$RESET."
log_gf_deleted = "$MAGENTA@{} (ID: {})$RESET deleted the goods file $YELLOWstorage/products/{}$RESET."
log_ar_added = "$MAGENTA@{} (ID: {})$RESET added new command $YELLOW{}$RESET."
log_ar_response_text_changed = "$MAGENTA@{} (ID: {})$RESET response text of command $YELLOW{}$RESET to $YELLOW\"{}\"$RESET."
log_ar_notification_text_changed = "$MAGENTA@{} (ID: {})$RESET notification text of command $YELLOW{}$RESET to $YELLOW\"{}\"$RESET."
log_ar_cmd_deleted = "$MAGENTA@{} (ID: {})$RESET deleted the command $YELLOW{}$RESET."
log_cfg_downloaded = "$MAGENTA@{} (ID: {})$RESET requested config $YELLOW{}$RESET."
log_tmplt_added = "$MAGENTA@{} (ID: {})$RESET added the answer template $YELLOW\"{}\"$RESET."
log_tmplt_deleted = "$MAGENTA@{} (ID: {})$RESET deleted the answer template $YELLOW\"{}\"$RESET."

# handlers.py logs
log_new_msg = "$MAGENTA┌──$RESET New message in chat with $YELLOW{} (CID: {}):"
log_sending_greetings = "User $YELLOW{} (CID: {})$RESET wrote for the first time! Sending greetings..."
log_new_cmd = "Received the command $YELLOW{}$RESET in the chat with the user $YELLOW{} (CID: {})$RESET."
ntfc_new_order = "💰 <b>New order:</b> <code>{}</code>\n\n<b><i>🙍‍♂️ Buyer:</i></b>  <code>{}</code>\n"\
                 "<b><i>💵 Order amount:</i></b>  <code>{}</code>\n<b><i>📇 ID:</i></b> <code>#{}</code>\n\n<i>{}</i>"
ntfc_new_order_not_in_cfg = "ℹ️ The goods will not be delivered because auto-delivery is not linked to the lot."
ntfc_new_order_ad_disabled = "ℹ️ The goods will not be delivered because auto-delivery is disabled in global switches."
ntfc_new_order_ad_disabled_for_lot = "ℹ️ The goods will not be delivered because auto-delivery is disabled for this item."
ntfc_new_order_user_blocked = "ℹ️ The goods will not be delivered, because the user is on the black list and the auto-delivery lock is on."
ntfc_new_order_will_be_delivered = "ℹ️ The product will be delivered as soon as possible."

# vertex.py logs
crd_proxy_detected = "Proxy detected."
crd_checking_proxy = "Running proxy checks..."
crd_proxy_err = "Failed to connect to the proxy. Make sure that the data is entered correctly."
crd_proxy_success = "Proxy verified successfully! Requests to FunPay will be sent from the IP address $YELLOW{}$RESET."
crd_acc_get_timeout_err = "Failed to load account data: Timeout exceeded."
crd_acc_get_unexpected_err = "An unexpected error occurred while retrieving account information."
crd_try_again_in_n_secs = "The next attempt is in {} seconds(-s)..."
crd_getting_profile_data = "Getting lots and categories data..."
crd_profile_get_timeout_err = "Failed to load account lots data: timeout exceeded."
crd_profile_get_unexpected_err = "An unexpected error occurred while retrieving data about the account's lots."
crd_profile_get_too_many_attempts_err = "An error occurred while getting data about the lots of the account: the number of attempts ({}) was exceeded."
crd_profile_updated = "Updated the information about profile lots $YELLOW({})$RESET and categories $YELLOW({})$RESET."
crd_tg_profile_updated = "Updated the information about profile lots $YELLOW({})$RESET and categories $YELLOW({})$RESET (Telegram Control Panel)."
crd_raise_time_err = "The $CYAN\"{}\"$RESET category lots could not be raised. FunPay says to wait about {}."
crd_raise_unexpected_err = "An unexpected error occurred while trying to raise $CYAN\"{}\"$RESET catgory lots. Next attempt in 10 seconds."
crd_raise_429_err = "Error 429 when raising lots of the $CYAN\"{}\"$RESET category. Pause for 10 seconds..."
crd_lots_raised = "All lots in the $CYAN\"{}\"$RESET category are raised!"
crd_raise_wait_3600 = "Next attempt in {}."
crd_msg_send_err = "An error occurred when sending a message to chat $YELLOW{}$RESET."
crd_msg_attempts_left = "Attempts left: $YELLOW{}$RESET."
crd_msg_no_more_attempts_err = "Failed to send a message to chat $YELLOW{}$RESET: the number of attempts exceeded."
crd_msg_sent = "Sent a message to the chat $YELLOW{}."
crd_session_timeout_err = "Failed to refresh session: timeout exceeded."
crd_session_unexpected_err = "An unexpected error occurred while refreshing the session."
crd_session_no_more_attempts_err = "Failed to refresh session: the number of attempts was exceeded."
crd_session_updated = "Session updated."
crd_raise_loop_started = "$CYANThe auto-raise loop is running (this does not mean that auto-raise are enabled)."
crd_raise_loop_not_started = "$CYANThe auto-raise loop was not started because there are no lots detected on the account."
crd_session_loop_started = "$CYANThe session refresh loop is running."
crd_handlers_registered = "The handlers from $YELLOW{}.py$RESET are registered."
crd_handler_err = "An error occurred in the handler's execution."
