class ResumeStoreSingleton():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ResumeStoreSingleton, cls).__new__(cls)
        return cls.instance
    
    def uploadResume():
        pass

    def getResume():
        pass