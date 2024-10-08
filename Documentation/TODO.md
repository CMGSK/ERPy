# Pending tasks:

## Overview:

This document will outline the pending tasks in the project.
Since this is on a very early stage, all of the current tasks will be top priority, since they are necessary things to
implement before even an alpha version is released.
Everyone is welcome to define tasks in here, although they should be uncategorized until their priority is discussed.

Priorities for development can be:

- High priority
- Mid priority
- Low priority
- Uncategorized

Categories for this tasks can be:

- **N**ecessity
- **F**eature
- **I**mprovement
- **B**ug
- **D**ocumentation

#### High Priority

- **N**: Define a module to import from .xls and similars
- **N**: Define paths for local/online database
- **N**: Define paths for different database engines
- **N**: Define proper table structures (The database structure will be provided by us, we do not plan on accepting
  integrator data, this is focused on small businesses)
- **N**: Design a proper way of handling the sales through the GUI (It currently sucks badly)
- **N**: Implement employee management module
- **N**: Implement employee ticketing module
- **N**: Implement or refactor if necessary the following functionalities within the current modules or in new ones:
  Overall financial reports, Expenses vs income reports, Stock tracking, Order tracking, Sales registration, Sales
  reports, Sales management, Contacts management
- **D**: Comment the code so people can understand how loud the screams inside my head are and therefore my code
- **F**: Create a util that store logging of the app processes for debug, history and so on, and place calls to it all
  over the codebase

#### Mid Priority

- **N**: Create an Log-in system for different workers
- **I**: Refactor the god damn file naming, im just too stupid for naming properly
- **F**: Create a configuration window that allow us to define the tables shape, and maybe other useful things such as
  colors, behaviours, and so on
- **I**: Polish the GUI

#### Low Priority

- **D**: Create a playground with different things from customtkinter to use as a reference and to know the different
- **I**: Define permissions for different roles of user
- **I**: Pytesting the whole thing would really be interesting
