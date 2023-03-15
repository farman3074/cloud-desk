# invoice types
# field in invoices table
# SECURITYADVANCE - Inserted at booking
# MONTHLY - Monthly customer invoice
# SPECIAL - Invoices generated for clearances or other mid month billing

# billing types
# selected while booking - applied on booking rates
# MONTHLY - Monthly billing starting 1st of every month
# WEEKLY - for 7 days
# DAILY - Daily billing
# HOURLY - mainly for resources (board rooms, projectors etc)

# scans DB and create invoice entries for billing between startdate and enddate for a member
# returns a list of dictionary entries for invoices created 
def creat_monthly_batch_invoices(startdate,enddate, memberid):
  return