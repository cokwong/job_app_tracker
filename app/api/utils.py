class Serialize:
    def user(self, user):
        if not user:
            return {}
        user = {'google_id': user.google_id,
                }

    def table(self, table, include_apps=False):
        if not table:
            return {}
        data = {'id': table.id,
                'name': table.name}
        if include_apps:
            data['applications'] = self.applications(table.apps)
        return data

    def tables(self, tables, include_apps=False):
        if not tables:
            return {}
        data = []
        for table in tables:
            data.append(self.table(table, include_apps))
        return data

    def application(self, app):
        if not app:
            return {}
        data = {'id': app.id,
                'company': app.company,
                'position': app.position,
                'url': app.url,
                'status': self.status(app.status)}
        return data

    def applications(self, apps):
        if not apps:
            return {}
        data = []
        for app in apps:
            data.append(self.application(app))
        return data

    def status(self, status):
        data = []
        for s in status:
            data.append(s.id)
