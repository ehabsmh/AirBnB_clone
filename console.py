#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex


class HBNBCommand(cmd.Cmd):
    """Entry point of the command interpreter"""

    prompt = ("(hbnb) ")

    def do_quit(self, cmd_line):
        """Quit command to exit the program"""
        return True
    # ___________________________________________________________________________

    def do_EOF(self, cmd_line):
        """Exits after receiving the EOF signal"""
        return True
    # ___________________________________________________________________________

    def emptyline(self):
        """an empty line + ENTER should not execute anything"""
        pass
    # ___________________________________________________________________________

    def do_create(self, cmd_line):
        """
            Create a new instance of class BaseModel and saves it
            to the JSON file and prints the id
        """
        if len(cmd_line) < 1:
            print("** class name missing **")
            return
        try:
            cmd_line = shlex.split(cmd_line)
            instance = globals()[cmd_line[0]]()
            instance.save()
            print(instance.id)

        except Exception:
            print("** class doesn't exist **")
    # ___________________________________________________________________________

    def do_show(self, cmd_line):
        """
            Print the string representation of an instance based on
            the class name and id
        """
        cmd_line = shlex.split(cmd_line)
        if len(cmd_line) < 1:
            print("** class name missing **")
            return
        if len(cmd_line) < 2:
            print("** instance id missing **")
            return
        try:
            eval(cmd_line[0])
        except NameError:
            print("** class doesn't exist **")
            return

        dict_of_obj = storage.all()
        k = "{}.{}".format(cmd_line[0], cmd_line[1])
        try:
            v = dict_of_obj[k]
            print(v)
        except KeyError:
            print("** no instance found **")
    # ___________________________________________________________________________

    def do_destroy(self, cmd_line):
        """
            Deletes an instance based on the class name and id
        """
        cmd_line = shlex.split(cmd_line)
        if len(cmd_line) < 1:
            print("** class name missing **")
            return
        elif len(cmd_line) < 2:
            print("** instance id missing **")
            return
        try:
            eval(cmd_line[0])
        except NameError:
            print("** class doesn't exist **")
            return

        dict_of_obj = storage.all()
        k = "{}.{}".format(cmd_line[0], cmd_line[1])
        try:
            del dict_of_obj[k]
        except KeyError:
            print("** no instance found **")
        storage.save()
    # ___________________________________________________________________________

    def do_all(self, cmd_line):
        """
            Prints all string representation of all instances
            based or not on the class name
        """
        list_of_obj = []

        try:
            if len(cmd_line) > 0:
                eval(cmd_line)
        except NameError:
            print("** class doesn't exist **")
            return
        for k, v in storage.all().items():
            if len(cmd_line) > 0:
                if type(v) is eval(cmd_line):
                    list_of_obj.append(v)
            else:
                list_of_obj.append(v)

        print(list_of_obj)
    # ___________________________________________________________________________

    def do_update(self, cmd_line):
        """
            Updates an instance based on the class name and id
            by adding or updating attribute
        """

        cmd_line = shlex.split(cmd_line)
        if len(cmd_line) < 1:
            print("** class name missing **")
            return
        elif len(cmd_line) < 2:
            print("** instance id missing **")
            return
        elif len(cmd_line) < 3:
            print("** attribute name missing **")
            return
        elif len(cmd_line) < 4:
            print("** value missing **")
            return
        try:
            eval(cmd_line[0])
        except NameError:
            print("** class doesn't exist **")
            return
        k = "{}.{}".format(cmd_line[0], cmd_line[1])

        try:
            v = storage.all()[k]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(v, cmd_line[2]))
            cmd_line[3] = attr_type(cmd_line[3])
        except AttributeError:
            pass
        setattr(v, cmd_line[2], cmd_line[3])
        storage.save()


if __name__ == "__main__":
    """Entry point for the loop"""
    HBNBCommand().cmdloop()
