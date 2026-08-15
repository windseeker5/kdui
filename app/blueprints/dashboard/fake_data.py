"""Static fake data used across the dashboard blueprint."""

CUSTOMERS = [
    {"id": 1, "name": "Acme Corp",       "email": "hello@acme.com",    "status": "Active",   "plan": "Pro",      "revenue": "$12,400", "joined": "2024-01-15"},
    {"id": 2, "name": "Globex",           "email": "info@globex.com",   "status": "Active",   "plan": "Starter",  "revenue": "$3,200",  "joined": "2024-02-20"},
    {"id": 3, "name": "Initech",          "email": "bill@initech.com",  "status": "Inactive", "plan": "Pro",      "revenue": "$8,750",  "joined": "2024-03-05"},
    {"id": 4, "name": "Umbrella Corp",    "email": "ops@umbrella.com",  "status": "Active",   "plan": "Enterprise","revenue": "$48,200","joined": "2024-01-02"},
    {"id": 5, "name": "Stark Industries", "email": "tony@stark.com",    "status": "Active",   "plan": "Enterprise","revenue": "$92,000","joined": "2023-11-10"},
    {"id": 6, "name": "Wayne Enterprises","email": "bruce@wayne.com",   "status": "Inactive", "plan": "Pro",      "revenue": "$21,500", "joined": "2024-04-18"},
    {"id": 7, "name": "Dunder Mifflin",   "email": "michael@dm.com",    "status": "Active",   "plan": "Starter",  "revenue": "$1,800",  "joined": "2024-05-01"},
    {"id": 8, "name": "Vandelay Ind.",    "email": "art@vandelay.com",  "status": "Active",   "plan": "Pro",      "revenue": "$6,300",  "joined": "2024-05-22"},
    {"id": 9, "name": "Nakatomi Corp",    "email": "ceo@nakatomi.com",  "status": "Active",   "plan": "Enterprise","revenue": "$34,800","joined": "2024-02-14"},
    {"id":10, "name": "Rekall Inc.",       "email": "doug@rekall.com",   "status": "Inactive", "plan": "Starter",  "revenue": "$900",    "joined": "2024-06-01"},
    {"id":11, "name": "Soylent Corp",      "email": "ceo@soylent.com",   "status": "Active",   "plan": "Pro",      "revenue": "$9,100",  "joined": "2024-03-28"},
    {"id":12, "name": "Cyberdyne Systems", "email": "info@cyberdyne.com","status": "Active",   "plan": "Enterprise","revenue": "$77,600","joined": "2024-01-30"},
]

RECENT_ACTIVITY = [
    {"icon": "user-plus",  "text": "Acme Corp signed up",            "time": "2 min ago"},
    {"icon": "dollar-sign","text": "Stark Industries upgraded to Enterprise","time": "14 min ago"},
    {"icon": "alert-circle","text":"Initech subscription cancelled",  "time": "1 hr ago"},
    {"icon": "mail",       "text": "Invoice sent to Umbrella Corp",   "time": "3 hr ago"},
    {"icon": "check",      "text": "Wayne Enterprises onboarding done","time": "yesterday"},
]

STATS = [
    {"label": "Total Revenue",    "value": "$316,550", "delta": "+18.2% from last month", "trend": "up"},
    {"label": "Active Customers", "value": "8",        "delta": "+2 this month",           "trend": "up"},
    {"label": "Churn Rate",       "value": "3.4%",     "delta": "-0.5% vs last month",     "trend": "up"},
    {"label": "Avg. Revenue / Customer", "value": "$39,569", "delta": "+$4,200 vs last month", "trend": "up"},
]
