# AI Interaction Log

## Interaction 1: Initial Tkinter Example & Database Integration Setup

**Date:** March 4, 2026

**Prompt:**
"Follow the guidelines in attached file. Come with examples on how to make an application using Tkinter, which will let us make our initiative tracker add and remove data from a later created database."

**Summary:**
Provided a complete, working Tkinter example for a D&D Initiative Tracker demonstrating:
- Object-Oriented Programming with `Character` and `InitiativeTracker` classes
- A functional GUI (`MainWindow` class) with add/remove character functionality
- Input validation and user feedback via message boxes
- Automatic sorting by initiative (highest first)
- Clean, readable code suitable for Level 3.G students
- Foundation ready for future database integration

**Key Features Demonstrated:**
1. **Character Class** - Represents a single character with name and initiative
2. **InitiativeTracker Class** - Manages the collection of characters and sorting logic
3. **MainWindow Class** - Handles all Tkinter GUI operations (input fields, listbox, buttons)
4. **Data Management** - Add and remove characters with proper validation
5. **UI Elements** - Entry widgets, listbox with scrollbar, buttons, labels, frames

**Code Structure Explanation:**
- Input fields accept character name and initiative value
- Characters are sorted automatically by initiative (highest first)
- Listbox displays all characters in turn order
- Remove button takes the selected character from the list
- Clear All button removes all characters with confirmation dialog

**State:** Completed

**Next Steps (for user):**
- Run `main.py` to test the GUI
- Once working, the data structure can be easily extended to save/load from database
- Database integration can use the existing `tracker.get_characters()` method to fetch data

---
