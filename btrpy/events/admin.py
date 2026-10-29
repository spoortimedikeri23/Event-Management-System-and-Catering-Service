from django.contrib import admin
from django.utils.html import format_html
from events.models import (
    EventsList, EventType, indoorimages, outdoorimages,
    veg_menu, non_veg_menu, FinalCateringDetails,
    ExtraMenuItem, Enquiry, OrderManagement
)

admin.site.site_header = "✨ Eventure Admin Suite"
admin.site.site_title = "Eventure Portal"
admin.site.index_title = "Eventure Operations & Management Dashboard"


@admin.register(EventsList)
class EventsListAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'name', 'formatted_price', 'short_description')
    search_fields = ('name', 'descriptions')
    list_per_page = 15

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 54px; height: 38px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #94a3b8; font-size: 12px;">No image</span>')
    thumbnail_preview.short_description = "Preview"

    def formatted_price(self, obj):
        return format_html('<strong style="color: #047857; font-weight: 600;">₹{}</strong>', f"{obj.price:,}")
    formatted_price.short_description = "Basic Price"

    def short_description(self, obj):
        if obj.descriptions and len(obj.descriptions) > 75:
            return obj.descriptions[:75] + "..."
        return obj.descriptions or "-"
    short_description.short_description = "Description"


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(indoorimages)
class IndoorImagesAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'eventName', 'event_type')
    list_filter = ('eventName', 'event_type')
    search_fields = ('eventName__name',)

    def thumbnail_preview(self, obj):
        if obj.indoorimg:
            return format_html(
                '<img src="{}" style="width: 60px; height: 42px; object-fit: cover; border-radius: 6px;" />',
                obj.indoorimg.url
            )
        return format_html('<span style="color: #94a3b8;">No photo</span>')
    thumbnail_preview.short_description = "Photo"


@admin.register(outdoorimages)
class OutdoorImagesAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'eventName', 'event_type')
    list_filter = ('eventName', 'event_type')
    search_fields = ('eventName__name',)

    def thumbnail_preview(self, obj):
        if obj.outdoorimg:
            return format_html(
                '<img src="{}" style="width: 60px; height: 42px; object-fit: cover; border-radius: 6px;" />',
                obj.outdoorimg.url
            )
        return format_html('<span style="color: #94a3b8;">No photo</span>')
    thumbnail_preview.short_description = "Photo"


@admin.register(veg_menu)
class VegMenuAdmin(admin.ModelAdmin):
    list_display = ('menu_badge', 'formatted_price', 'item_preview')
    list_filter = ('menu_number',)
    ordering = ('menu_number',)

    def menu_badge(self, obj):
        return format_html(
            '<span style="background: #ecfdf5; color: #047857; font-weight: 700; padding: 4px 10px; border-radius: 9999px; font-size: 12px; border: 1px solid #a7f3d0;">🥦 Menu #{}</span>',
            obj.menu_number
        )
    menu_badge.short_description = "Menu Tier"

    def formatted_price(self, obj):
        return format_html('<strong>₹{} / head</strong>', f"{obj.price:,}")
    formatted_price.short_description = "Price per Head"

    def item_preview(self, obj):
        if len(obj.item) > 80:
            return obj.item[:80] + "..."
        return obj.item
    item_preview.short_description = "Dishes Included"


@admin.register(non_veg_menu)
class NonVegMenuAdmin(admin.ModelAdmin):
    list_display = ('menu_badge', 'formatted_price', 'item_preview')
    list_filter = ('menu_number',)
    ordering = ('menu_number',)

    def menu_badge(self, obj):
        return format_html(
            '<span style="background: #fff1f2; color: #be123c; font-weight: 700; padding: 4px 10px; border-radius: 9999px; font-size: 12px; border: 1px solid #fecdd3;">🍗 Menu #{}</span>',
            obj.menu_number
        )
    menu_badge.short_description = "Menu Tier"

    def formatted_price(self, obj):
        return format_html('<strong>₹{} / head</strong>', f"{obj.price:,}")
    formatted_price.short_description = "Price per Head"

    def item_preview(self, obj):
        if len(obj.item) > 80:
            return obj.item[:80] + "..."
        return obj.item
    item_preview.short_description = "Dishes Included"


@admin.register(ExtraMenuItem)
class ExtraMenuItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'type_badge')
    list_filter = ('type',)
    search_fields = ('item',)

    def type_badge(self, obj):
        if obj.type == 'veg':
            return format_html('<span style="background: #ecfdf5; color: #065f46; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">Veg</span>')
        return format_html('<span style="background: #fff1f2; color: #9f1239; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">Non-Veg</span>')
    type_badge.short_description = "Type"


@admin.register(FinalCateringDetails)
class FinalCateringDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'event_name', 'event_type_badge', 'total_people',
        'food_type_badge', 'menu_type_badge', 'no_of_suppliers',
        'cake_required', 'addons_summary'
    )
    list_filter = ('food_type', 'event_type', 'menu_type', 'welcome_drinks', 'welcome_chats', 'pan')
    search_fields = ('event_name',)
    list_per_page = 20

    def event_type_badge(self, obj):
        bg = "#e0e7ff" if obj.event_type.lower() == "indoor" else "#fef3c7"
        color = "#3730a3" if obj.event_type.lower() == "indoor" else "#92400e"
        return format_html(
            '<span style="background: {}; color: {}; padding: 3px 9px; border-radius: 6px; font-weight: 600; font-size: 11px; text-transform: uppercase;">{}</span>',
            bg, color, obj.event_type
        )
    event_type_badge.short_description = "Venue Type"

    def food_type_badge(self, obj):
        if obj.food_type == 'veg':
            return format_html('<span style="background: #ecfdf5; color: #047857; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 11px;">🥦 Veg</span>')
        return format_html('<span style="background: #fff1f2; color: #be123c; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 11px;">🍗 Non-Veg</span>')
    food_type_badge.short_description = "Food Type"

    def menu_type_badge(self, obj):
        return format_html('<span style="font-weight: 600;">Menu #{}</span>', obj.menu_type)
    menu_type_badge.short_description = "Menu Tier"

    def addons_summary(self, obj):
        badges = []
        if obj.welcome_drinks:
            badges.append('<span style="background: #dbeafe; color: #1e40af; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-right: 2px;">🍹 Drinks</span>')
        if obj.welcome_chats:
            badges.append('<span style="background: #fef3c7; color: #92400e; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-right: 2px;">🍟 Chats</span>')
        if obj.pan:
            badges.append('<span style="background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; font-size: 10px;">🍃 Pan</span>')
        if not badges:
            return format_html('<span style="color: #94a3b8; font-size: 11px;">None</span>')
        return format_html("".join(badges))
    addons_summary.short_description = "Add-ons"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_link', 'phone_link', 'short_message')
    search_fields = ('name', 'email', 'phone', 'message')

    def email_link(self, obj):
        return format_html('<a href="mailto:{}" style="color: #4f46e5; text-decoration: underline;">{}</a>', obj.email, obj.email)
    email_link.short_description = "Email"

    def phone_link(self, obj):
        return format_html('<a href="tel:{}" style="color: #059669; font-weight: 600;">📞 {}</a>', obj.phone, obj.phone)
    phone_link.short_description = "Phone"

    def short_message(self, obj):
        if len(obj.message) > 60:
            return obj.message[:60] + "..."
        return obj.message
    short_message.short_description = "Inquiry Message"


@admin.register(OrderManagement)
class OrderManagementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'event_name_display', 'food_summary', 'basic_price_formatted',
        'catering_cost_formatted', 'gst_formatted', 'total_cost_badge', 'created_at_formatted'
    )
    list_filter = (
        'created_at',
        'catering_detail__food_type',
        'catering_detail__event_type'
    )
    search_fields = ('catering_detail__event_name', 'catering_detail__food_type')
    date_hierarchy = 'created_at'
    list_per_page = 20

    def event_name_display(self, obj):
        detail = obj.catering_detail
        return format_html(
            '<div style="line-height: 1.3;"><strong style="color: #1e293b; font-size: 13px;">{}</strong><br>'
            '<span style="font-size: 11px; color: #64748b;">{} | {} Guests</span></div>',
            detail.event_name, detail.event_type.capitalize(), detail.total_people
        )
    event_name_display.short_description = "Event Booking"

    def food_summary(self, obj):
        detail = obj.catering_detail
        if detail.food_type == 'veg':
            return format_html('<span style="color: #047857; font-weight: 600;">🥦 Veg (Menu #{})</span>', detail.menu_type)
        return format_html('<span style="color: #be123c; font-weight: 600;">🍗 Non-Veg (Menu #{})</span>', detail.menu_type)
    food_summary.short_description = "Catering"

    def basic_price_formatted(self, obj):
        return format_html('<span>₹{}</span>', f"{int(obj.basic_package_price):,}")
    basic_price_formatted.short_description = "Base Package"

    def catering_cost_formatted(self, obj):
        return format_html('<span>₹{}</span>', f"{int(obj.total_menu_price):,}")
    catering_cost_formatted.short_description = "Menu Cost"

    def gst_formatted(self, obj):
        return format_html('<span style="color: #64748b;">₹{}</span>', f"{round(obj.gst, 2):,}")
    gst_formatted.short_description = "GST (6%)"

    def total_cost_badge(self, obj):
        return format_html(
            '<span style="background: #ecfdf5; color: #047857; font-weight: 700; font-size: 13px; padding: 4px 10px; border-radius: 6px; border: 1px solid #a7f3d0; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">'
            '₹{}'
            '</span>',
            f"{round(obj.total_cost, 2):,}"
        )
    total_cost_badge.short_description = "Grand Total"

    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %b %Y, %I:%M %p")
    created_at_formatted.short_description = "Booked On"
