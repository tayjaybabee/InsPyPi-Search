class TableColumnsLockedError(Exception):
    print(
        'The table you are trying to add a column to is locked to only allow adding rows now.'
    )
