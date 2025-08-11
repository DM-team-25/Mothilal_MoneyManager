
from models.group_model import GroupMemberModel, GroupExpenseModel
from utils.print_service import display_message

class GroupService:

    @staticmethod
    def create_group(group_name, user_id):
        success = GroupExpenseModel.create_group(group_name, user_id)
        if success:
            group = GroupExpenseModel.get_group_by_name(group_name)
            if group:
                GroupMemberModel.add_member(group['id'], user_id)  # Add creator as member
            display_message(f"Group '{group_name}' created successfully.")
        else:
            display_message("Failed to create group. It may already exist.")

    @staticmethod
    def add_member_to_group(group_id, user_id):
        success = GroupMemberModel.add_member(group_id, user_id)
        if success:
            display_message("Member added successfully.")
        else:
            display_message("Failed to add member. Maybe already a member or invalid IDs.")

    @staticmethod
    def list_groups(user_id=None):
        if user_id is None:
            display_message("User ID is required to list groups.")
            return []

        groups = GroupExpenseModel.get_groups_by_user(user_id)
        if not groups:
            display_message("No groups found.")
            return []

        print("\nYour Groups:")
        for group in groups:
            print(f"ID: {group['id']}, Name: {group['name']}")
        return groups

    @staticmethod
    def list_group_members(group_id):
        members = GroupMemberModel.get_members_by_group(group_id)
        if not members:
            display_message("No members found or invalid group ID.")
            return []

        print(f"\nMembers of Group ID {group_id}:")
        for member in members:
            print(f"User ID: {member['user_id']}, Username: {member['username']}")
        return members

    @staticmethod
    def add_group_expense(group_id, user_id, amount, category, description, date, shares):
        expense_id = GroupExpenseModel.add_expense(group_id, user_id, amount, category, description, date)
        if expense_id:
            shares_added = GroupMemberModel.add_expense_shares(expense_id, shares)
            if shares_added:
                display_message("Group expense and shares added successfully.")
            else:
                display_message("Group expense added, but failed to add shares.")
        else:
            display_message("Failed to add group expense.")

    @staticmethod
    def view_group_expenses(group_id):
        expenses = GroupExpenseModel.get_expenses_by_group(group_id)
        if not expenses:
            display_message("No expenses found for this group.")
            return

        print(f"\nExpenses for Group ID {group_id}:")
        for exp in expenses:
            print(f"ID: {exp['id']}, Paid By User ID: {exp['paid_by_user_id']} ({exp['username']}), Amount: {exp['amount']}, "
                  f"Category: {exp['category']}, Description: {exp['description']}, Date: {exp['date']}")
