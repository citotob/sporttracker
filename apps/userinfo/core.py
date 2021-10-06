#Core Computing Algorithm
class Core(object):
      __instance = None
      m_isCommon = False
      #Singleton pattern
      def __new__(cls):
            if not cls.__instance:
                  cls.__instance = object.__new__(cls)
            return cls.__instance

      def core(self,bet):
        pass

coreinstance = Core()      