"""Tkinter reference app for common pandas and NumPy APIs."""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Iterable, List


@dataclass(frozen=True)
class ReferenceEntry:
    library: str
    name: str
    signature: str
    description: str
    example: str


REFERENCE_ENTRIES: List[ReferenceEntry] = [
    ReferenceEntry(
        library="NumPy",
        name="numpy.array",
        signature="numpy.array(object, dtype=None, *, copy=True, ndmin=0)",
        description="Create an ndarray from array-like input.",
        example="import numpy as np\narr = np.array([[1, 2], [3, 4]], dtype=float)",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.arange",
        signature="numpy.arange(start, stop=None, step=1, dtype=None)",
        description="Create evenly spaced values within a given interval.",
        example="np.arange(0, 10, 2)  # array([0, 2, 4, 6, 8])",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.linspace",
        signature="numpy.linspace(start, stop, num=50, endpoint=True)",
        description="Return evenly spaced numbers over a specified interval.",
        example="np.linspace(0.0, 1.0, num=5)  # array([0. , 0.25, 0.5 , 0.75, 1. ])",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.zeros",
        signature="numpy.zeros(shape, dtype=float)",
        description="Return a new array of given shape and type, filled with zeros.",
        example="np.zeros((2, 3))",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.ones",
        signature="numpy.ones(shape, dtype=float)",
        description="Return a new array of given shape and type, filled with ones.",
        example="np.ones(5, dtype=int)  # array([1, 1, 1, 1, 1])",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.eye",
        signature="numpy.eye(N, M=None, k=0, dtype=float)",
        description="Return a 2-D array with ones on the diagonal and zeros elsewhere.",
        example="np.eye(3)  # 3x3 identity matrix",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.reshape",
        signature="ndarray.reshape(newshape, order='C')",
        description="Give a new shape to an array without changing its data.",
        example="np.arange(6).reshape(2, 3)",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.concatenate",
        signature="numpy.concatenate((a1, a2, ...), axis=0)",
        description="Join a sequence of arrays along an existing axis.",
        example="np.concatenate([np.array([1, 2]), np.array([3, 4])])",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.mean",
        signature="numpy.mean(a, axis=None)",
        description="Compute the arithmetic mean along the specified axis.",
        example="np.mean(np.array([[1, 2], [3, 4]]), axis=0)  # array([2., 3.])",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.std",
        signature="numpy.std(a, axis=None, ddof=0)",
        description="Compute the standard deviation along the specified axis.",
        example="np.std(np.array([1, 2, 3]))  # 0.816496580927726",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.dot",
        signature="numpy.dot(a, b, out=None)",
        description="Dot product of two arrays.",
        example="np.dot(np.array([1, 2]), np.array([3, 4]))  # 11",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.matmul",
        signature="numpy.matmul(x1, x2)",
        description="Matrix product of two arrays.",
        example="np.matmul(np.eye(2), np.ones((2, 2)))",
    ),
    ReferenceEntry(
        library="NumPy",
        name="numpy.where",
        signature="numpy.where(condition, x=None, y=None)",
        description="Return elements chosen from x or y depending on condition.",
        example="np.where(arr > 0, 'positive', 'non-positive')",
    ),
    ReferenceEntry(
        library="pandas",
        name="pandas.Series",
        signature="pandas.Series(data=None, index=None, dtype=None)",
        description="One-dimensional labeled array capable of holding any data type.",
        example="import pandas as pd\nser = pd.Series([10, 20, 30], index=['a', 'b', 'c'])",
    ),
    ReferenceEntry(
        library="pandas",
        name="pandas.DataFrame",
        signature="pandas.DataFrame(data=None, index=None, columns=None)",
        description="Two-dimensional, size-mutable, heterogeneous tabular data structure.",
        example="df = pd.DataFrame({'name': ['Ana', 'Ben'], 'score': [92, 85]})",
    ),
    ReferenceEntry(
        library="pandas",
        name="pandas.read_csv",
        signature="pandas.read_csv(filepath, sep=',', dtype=None, parse_dates=None)",
        description="Read a comma-separated values file into a DataFrame.",
        example="df = pd.read_csv('customers.csv', parse_dates=['joined_at'])",
    ),
    ReferenceEntry(
        library="pandas",
        name="pandas.read_excel",
        signature="pandas.read_excel(io, sheet_name=0)",
        description="Read an Excel file into a DataFrame.",
        example="df = pd.read_excel('report.xlsx', sheet_name='Summary')",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.head",
        signature="DataFrame.head(n=5)",
        description="Return the first n rows of the DataFrame.",
        example="df.head(3)",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.describe",
        signature="DataFrame.describe(percentiles=None, include=None, exclude=None)",
        description="Generate descriptive statistics for numeric (and optionally categorical) columns.",
        example="df.describe(include='all')",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.groupby",
        signature="DataFrame.groupby(by=None, axis=0, as_index=True)",
        description="Group DataFrame using a mapper or by a Series of columns.",
        example="df.groupby('region')['sales'].sum()",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.merge",
        signature="DataFrame.merge(right, how='inner', on=None)",
        description="Merge DataFrame objects with a database-style join.",
        example="orders.merge(customers, how='left', on='customer_id')",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.pivot_table",
        signature="DataFrame.pivot_table(values=None, index=None, columns=None, aggfunc='mean')",
        description="Create a spreadsheet-style pivot table as a DataFrame.",
        example="df.pivot_table(values='sales', index='region', columns='channel', aggfunc='sum')",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.apply",
        signature="DataFrame.apply(func, axis=0, result_type=None)",
        description="Apply a function along an axis of the DataFrame.",
        example="df.apply(lambda col: col.max() - col.min())",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.loc",
        signature="DataFrame.loc[row_indexer, column_indexer]",
        description="Label-based selection of rows and columns.",
        example="df.loc['2019-01-01':'2019-01-07', ['sales', 'cost']]",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.iloc",
        signature="DataFrame.iloc[row_indexer, column_indexer]",
        description="Selection by integer position.",
        example="df.iloc[0:5, 1:3]",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.assign",
        signature="DataFrame.assign(**kwargs)",
        description="Assign new columns to a DataFrame and return a new object.",
        example="df.assign(total=df['price'] * df['qty'])",
    ),
    ReferenceEntry(
        library="pandas",
        name="DataFrame.to_csv",
        signature="DataFrame.to_csv(path_or_buf=None, index=True)",
        description="Write object to a comma-separated values file.",
        example="df.to_csv('export.csv', index=False)",
    ),
]


class ReferenceApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Pandas & NumPy Reference")
        self.root.geometry("960x600")
        self.root.configure(background="black")

        self.search_var = tk.StringVar()
        self.filtered_entries: List[ReferenceEntry] = sorted(
            REFERENCE_ENTRIES,
            key=lambda entry: (entry.library.lower(), entry.name.lower()),
        )

        self._build_layout()
        self._populate_list()

    def _build_layout(self) -> None:
        header = ttk.Frame(self.root, padding=(16, 12))
        header.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(
            header,
            text="Pandas & NumPy Reference",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor=tk.W)

        search_frame = ttk.Frame(header)
        search_frame.pack(anchor=tk.W, pady=(8, 0))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 8))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side=tk.LEFT)
        search_entry.bind("<KeyRelease>", self._on_search)

        paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        list_frame = ttk.Frame(paned, padding=(0, 0, 12, 0))
        detail_frame = ttk.Frame(paned)
        paned.add(list_frame, weight=1)
        paned.add(detail_frame, weight=2)

        self.listbox = tk.Listbox(
            list_frame,
            exportselection=False,
            activestyle="none",
            font=("Segoe UI", 11),
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_selection)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        self.detail_text = tk.Text(
            detail_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            background="#111111",
            foreground="#f5f5f5",
            relief=tk.FLAT,
            padx=16,
            pady=16,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        self.detail_text.configure(state=tk.DISABLED)

    def _populate_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for entry in self.filtered_entries:
            self.listbox.insert(tk.END, f"{entry.library} :: {entry.name}")
        if self.filtered_entries:
            self.listbox.selection_set(0)
            self._show_entry(self.filtered_entries[0])

    def _on_search(self, _event: tk.Event) -> None:
        term = self.search_var.get().strip().lower()
        if not term:
            self.filtered_entries = sorted(
                REFERENCE_ENTRIES,
                key=lambda entry: (entry.library.lower(), entry.name.lower()),
            )
        else:
            def matches(entry: ReferenceEntry) -> bool:
                haystack = " ".join(
                    [entry.library, entry.name, entry.signature, entry.description]
                ).lower()
                return term in haystack

            self.filtered_entries = [entry for entry in REFERENCE_ENTRIES if matches(entry)]
            self.filtered_entries.sort(key=lambda entry: (entry.library.lower(), entry.name.lower()))
        self._populate_list()

    def _on_selection(self, _event: tk.Event) -> None:
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            return
        entry = self.filtered_entries[index]
        self._show_entry(entry)

    def _show_entry(self, entry: ReferenceEntry) -> None:
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        sections = [
            f"Library: {entry.library}\n",
            f"Name: {entry.name}\n",
            f"Signature:\n  {entry.signature}\n\n",
            f"What it does:\n  {entry.description}\n\n",
            "Example:\n",
            "  " + "\n  ".join(entry.example.splitlines()) + "\n",
        ]
        for section in sections:
            self.detail_text.insert(tk.END, section)
        self.detail_text.configure(state=tk.DISABLED)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    ReferenceApp().run()


if __name__ == "__main__":
    main()
