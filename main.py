import monday_tools
from secret import mondayAPIkey



# # the variable response is data that is  some items we need to delete from a monday.com board( task manager solutions we use)

query = '{boards(ids: 1796452793) {groups(ids: "new_group"){items{id}}}}'
response = monday_tools.send_query(mondayAPIkey, query )

# we can use the monday_tools.send_query  function to also delete these items the query need to recieve the item id in order to delete it
# here is the necessary grapghQL query in order to delte an item 



# mutation{
#   delete_item(item_id:1860501522) {
#     id
#   }
# }


# you need to pass every id from response through that queery to clean out this board daily.
