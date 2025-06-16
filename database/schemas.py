def individual_data(todo):
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "status": todo["is_completed"],
        "creation": todo["creation"],
        "updated_at": todo["updated_at"],
    }


def all_tasks(todos):
    return [individual_data(todo) for todo in todos]
