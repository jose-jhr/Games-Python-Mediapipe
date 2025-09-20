from abc import abstractmethod,ABC


class InterfacePuntajeMet(ABC):
    @abstractmethod
    def responsePuntaje(self,puntaje)->str:
        pass