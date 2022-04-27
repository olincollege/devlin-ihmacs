"""
Ihmacs buffer implementation.
"""


class Buffer:
    """
    Ihmacs text buffer.

    Attributes:
        text: A string representing the buffer text.
        modified: A bool representing if the buffer has been modified since
            last save.
        point: An int representing cursor position in file.
        mark: An int representing the mark position in file. Used to define
            the region.
        name: A string representing the buffer name
        path: A string representing the file path on the system associated with
            the buffer. This is the file the buffer is saved to.
        major_mode: A major mode type representing the active major mode.
        minor_modes: A list of minor modes representing the active minor modes.
        keymap: not decided yet, but a sort of tree structure mapping inputted
            keychords to editing methods. Are first class methods a thing or am
            I about to put myself into a world of hell?
        command_history: A list of functions/methods that have been executed
            since last save.
        modeline: A string who's format method will generate a modeline. It can
            display information about the buffer as well as information about
            active modes by their "lighter" string.
        display_line: An int representing which line in the buffer is to be
            displayed as the first line of a window in the view.
    """

    def __init__(self, name="**", path=""):
        """
        Initialize buffer instance.

        Args:
            name: Keyarg, a string representing the buffer name.
            path: Keyarg, a string representing the associated file path.
        """
        self._text = ""
        self._modified = False
        self._point = 0
        self._mark = 0
        self._name = name
        self._path = path
        # self.major_mode = instance of fundamental mode
        self.minor_modes = []
        # self.keymap = dict of dicts, I'll get to this when I get to this.
        self.command_history = []
        self.modeline = ""
        self.display_line = 0

        # If path was passed load file
        # if self.path != "":
        # TODO: Add error handling for if the file does not exist yet
        # self.revert()

    # Properties
    @property
    def text(self):
        """
        Return text in buffer.
        """
        return self._text

    @property
    def modified(self):
        """
        Return modification state of buffer.
        """
        return self._modified

    @property
    def point(self):
        """
        Return position of point in buffer.
        """
        return self._point

    @property
    def mark(self):
        """
        Return position of mark in buffer.
        """
        return self._mark

    @property
    def name(self):
        """
        Return name of buffer.
        """
        return self._name

    @property
    def path(self):
        """
        Return associated file path of buffer.
        """
        return self._path

    # Helper methods
    def _normalize_pos(self, pos):
        """
        Normalize a point to ensure it lies in the range of the buffer.

        The range of the buffer is from 0 to the length of the text.

        Args:
            pos: An int representing a point in the buffer.

        Returns:
            An int between 0 and the length of the text in the buffer.
        """
        return max(0, min(pos, len(self.text)))

    # Disk operations
    def revert(self):
        """
        Revert buffer by reloading associated file.

        If the file does not exist, print error to *messages* buffer.

        Returns:
            A bool representing whether or not the revert was successful.
        """
        pass

    def save_buffer(self):
        """
        Save modified buffer to associated path.

        Updates modified state to False.
        """
        pass

    def write_file(self, path):
        """
        Update associated path and write buffer to new associated path.

        Updates modified state to False.
        """
        pass

    # Movement
    def set_point(self, pos):
        """
        Set point to position in buffer.

        Args:
           pos: An int representing where in the buffer to set point.
        """
        pos = self._normalize_pos(pos)
        self._point = pos

    def set_mark(self, pos):
        """
        Set mark to position in buffer.

        Args:
            pos: An int representing where in the buffer to set mark.
        """
        pos = self._normalize_pos(pos)
        self._mark = pos

    # Base editing operations. These all return values because that will
    # be useful for say, pushing to the kill ring.

    def insert(self, *args):
        """
        Insert args at point in buffer.

        Updates state of _text, _point, and _mark attributes.

        Args:
            args: A tuple of strings to insert.

        Returns:
            A string representing the inserted text.
        """
        point = self.point
        mark = self.mark

        insert_text = "".join(args)
        insert_len = len(insert_text)

        # The side effects
        self._text = self.text[:point] + insert_text + self.text[point:]
        self._point = point + insert_len

        if mark > point:
            self._mark = mark + insert_len

        # Return inserted text
        return insert_text

    def delete_char(self, chars=1):
        """
        Delete characters from buffer at point.

        Updates state of _text, _point, and _mark attributes.

        Args:
            chars: Number of characters to delete. If positive, delete
                characters after point. If negative, delete characters before
                point.

        Returns:
            A string containing the deleted text.
        """
        points = (self.point, self._normalize_pos(self.point + chars))

        # Rearrange due to negative args
        start = min(points)
        end = max(points)

        # Info about what we are deleting
        deleted_text = self.text[start:end]
        deleted_len = len(deleted_text)

        # The side effects
        self._text = self.text[:start] + self.text[end:]

        # If deleting text before point, move point backwards
        if chars < 0:
            self._point = start

        # Handle the mark, move as would be expected
        mark = self.mark

        if start <= mark <= end:
            self._mark = start
        elif mark > end:
            self._mark = mark - deleted_len

        # Return deleted text
        return deleted_text

    def delete_region(self):
        """
        Delete text in region defined by point and mark.

        Updates state of _text, _point, and _mark attributes.

        Returns:
            A string containing all the deleted text.
        """
        start = min(self.point, self.mark)
        end = max(self.point, self.mark)

        deleted_text = self.text[start:end]

        # Side effects
        self._text = self.text[:start] + self.text[end:]
        self._point = start
        self._mark = start

        # Handle the return
        return deleted_text