from PySide6.QtCore import QSettings


class SupervisorDAO:
    def __init__(self):
        self.settings_supervisor = QSettings('JEN-LIFE', 'PIM_SUPERVISOR')
        self.settings_just_enroll = QSettings('JEN-LIFE', 'PIM_JUST_ENROLL')

        self._supervisorInfo = self.settings_supervisor.value('supervisorInfo', {})
        self._justEnroll = self.settings_just_enroll.value('justEnroll', {})

    @property
    def supervisorInfo(self):
        return self._supervisorInfo

    @supervisorInfo.setter
    def supervisorInfo(self, supervisor_info):
        self._supervisorInfo = supervisor_info
        self.settings_supervisor.setValue('supervisorInfo', supervisor_info)

    @property
    def sv_username(self):
        return self._supervisorInfo.get('username')

    @property
    def sv_name(self):
        return self._supervisorInfo.get('name')

    @property
    def sv_birthDate(self):
        return self._supervisorInfo.get('birthDate')

    @property
    def sv_gender(self):
        return self._supervisorInfo.get('gender')

    @property
    def sv_organization(self):
        return self._supervisorInfo.get('organization')

    @property
    def sv_email(self):
        return self._supervisorInfo.get('email')

    @property
    def sv_rememberMe(self):
        return self._supervisorInfo.get('remember')

    @property
    def justEnroll(self):
        return self._justEnroll

    @justEnroll.setter
    def justEnroll(self, just_enroll):
        self._justEnroll = just_enroll
        self.settings_just_enroll.setValue('justEnroll', just_enroll)

    @property
    def je_chartNum(self):
        return self._justEnroll.get('chartNum')

    @property
    def je_name(self):
        return self._justEnroll.get('name')

    @property
    def je_professor(self):
        return self._justEnroll.get('professor')

    @property
    def je_searchFrom(self):
        return self._justEnroll.get('searchFrom')

    @property
    def je_searchTo(self):
        return self._justEnroll.get('searchTo')