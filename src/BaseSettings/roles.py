from rolepermissions.roles import AbstractUserRole

class SystemAdmin(AbstractUserRole):
    available_permissions = {
        'drop_tables': True,
    }

class OrganismAdmin(AbstractUserRole):
    available_permissions = {
        'create_organism': True,
    }

class Researcher(AbstractUserRole):
    available_permissions = {
        'edit_specie': True,
    }

class StateAgency(AbstractUserRole):
    available_permissions = {
        'add_specimen': True,
    }


class Other(AbstractUserRole):
    available_permissions = {
        'view_data': True,
    }
