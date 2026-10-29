from django import template
from django.db.models import Sum
from django.contrib.auth.models import User
from events.models import OrderManagement, EventsList, Enquiry, FinalCateringDetails

register = template.Library()

@register.simple_tag
def get_admin_metrics():
    orders = OrderManagement.objects.all().order_by('-created_at')
    total_orders = orders.count()
    revenue_agg = orders.aggregate(total=Sum('total_cost'))
    total_revenue = revenue_agg['total'] or 0
    total_users = User.objects.count()
    total_events = EventsList.objects.count()
    total_enquiries = Enquiry.objects.count()
    recent_orders = orders.select_related('catering_detail')[:6]
    recent_enquiries = Enquiry.objects.all().order_by('-id')[:5]

    return {
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2),
        'total_users': total_users,
        'total_events': total_events,
        'total_enquiries': total_enquiries,
        'recent_orders': recent_orders,
        'recent_enquiries': recent_enquiries,
    }
