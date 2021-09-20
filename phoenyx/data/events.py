from typing import Callable, Union


class Events:
    """
    random object structure to handle events
    """
    def __init__(self, renderer) -> None:
        self._renderer = renderer

    def get(self, name: Union[str, int]) -> Union[bool, int, float, str]:
        """
        gets an event result by name or id\\
        note that terminated events will have their name removed (id is untouched)\\
        result might be None

        Parameters
        ----------
            name : Union[str, int]
                name or id of the event

        Returns
        -------
            Union[bool, int, float, str] : result
        """
        events: dict[int, tuple[str, Union[bool, int, float,
                                           str]]] = self._renderer._all_events
        if isinstance(name, str):
            for _, v in events.items():
                if v[0] == name:
                    return v[1]
        elif isinstance(name, int):
            for k, v in events.items():
                if k == name:
                    return v[1]

    def get_id_by_name(self, name: str) -> int:
        """
        gets an event unique id by its name

        Parameters
        ----------
            name : str
                name of the event

        Returns
        -------
            int : unique id
        """
        events: dict[int, tuple[str, Union[bool, int, float,
                                           str]]] = self._renderer._all_events
        for k, v in events.items():
            if v[0] == name:
                return k

    def get_name_by_id(self, id: int) -> str:
        """
        gets an event name by its unique id

        Parameters
        ----------
            id : int
                unique id

        Returns
        -------
            str : name of the event
        """
        events: dict[int, tuple[str, Union[bool, int, float,
                                           str]]] = self._renderer._all_events
        for k, v in events.items():
            if k == id:
                return v[0]

    def list(self) -> list[tuple[str, int, str]]:
        """
        gets a list of non terminated events

        Returns
        -------
            list[tuple[str, int, str]] : name, unique_id, state
        """
        l: list[tuple[str, int, str]] = []
        events: dict[str, tuple[int, Union[bool, int, float,
                                           str]]] = self._renderer._all_events
        for k, v in events.items():
            if v[0] != "":
                state = "running" if v[1] is None else "done"
                l.append((v[0], k, state))
        return l

    def new(self, name: str, act: Callable[[], None]) -> None:
        """
        new event handled by the user
        
        Parameters
        ----------
            name : str
                name of the event
            act : Callable[[], None]
                activation/trigger function
        """
        self._renderer._last_event_id += 1
        k = self._renderer._last_event_id
        self._renderer._all_events[k] = (name, None)
        self._renderer._events_act[k] = act
