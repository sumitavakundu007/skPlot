import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from tkinter.filedialog import askopenfile
from tkinter.ttk import Combobox
import subprocess
from tkinter import messagebox
from subprocess import Popen, PIPE
import os
from PIL import ImageTk, Image, ImageDraw
import time, sys
import concurrent.futures
from mpl_toolkits.axisartist.axislines import Subplot
from matplotlib.colors import Normalize 
from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure
import matplotlib.animation as anim
import types
import mpl_interactions.ipyplot as iplt
from mpl_interactions import ioff, panhandler, zoom_factory
from IPython.display import display

class plot_save:
    def __init__(self, window):
        self.window = window
        self.xLabel = StringVar()
        self.yLabel = StringVar()
        self.zLabel = StringVar()
        self.xLower = DoubleVar()
        self.xUpper = DoubleVar()
        self.yLower = DoubleVar()
        self.yUpper = DoubleVar()
        self.zLower = DoubleVar()
        self.zUpper = DoubleVar()
        self.xFig = DoubleVar()
        self.yFig = DoubleVar()
        self.xy = StringVar()
        self.xy_ticks = StringVar()
        self.tk_len = DoubleVar()
        self.xyticks_len = DoubleVar()
        self.tkFont = DoubleVar()
        self.tk_xbin = IntVar()
        self.tk_ybin = IntVar()
        self.tk_zbin = IntVar()
        self.bin_var = DoubleVar()
        self.range_var_low = DoubleVar()
        self.range_var_high = DoubleVar()
        self.density_var = StringVar()
        self.width_var = DoubleVar()
        self.color_var = StringVar()
        self.num_cols = 0
        self.widthbar = DoubleVar()
        self.lgd_string = StringVar()
        self.colormap_name = StringVar()
        self.colorbar_req = StringVar()
        self.colorbar_label = DoubleVar()
        self.x_arr, self.y_arr = [], []
        self.filePaths = []

        self.fig = Figure(figsize=(3, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        self.toolbar.update()

    def upload_file(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        files = filedialog.askopenfilenames(multiple=True)
        var = window.tk.splitlist(files)
        for f in var:
            self.filePaths.append(f)

        self.new_var_arr = [IntVar() for i in range(len(self.filePaths))]
        self.legend_var_arr = [IntVar() for i in range(len(self.filePaths))]
        self.lgdFont = IntVar()
        self.lgdLoc = StringVar()
        self.marker_var_arr = [IntVar() for i in range(len(self.filePaths))]
        self.marker_size_var_arr = [IntVar() for i in range(len(self.filePaths))]
        self.linewidth_var_arr = [IntVar() for i in range(len(self.filePaths))]

        self.fig = Figure(figsize=(3, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        self.toolbar.update()
        plot_msgbox = messagebox.showinfo("Instructions", "Click \"Line plot\", \"Line-point\", \"Histogram plot\", \"3D plot\", \"Color z-axis\", or \"Scatter plot\" to plot the files ")

    def plot_file(self):
        if len(self.filePaths) >= 1:
            # Destroy the window
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            self.num_cols = 2
            for i in self.filePaths:
                self.x_arr.append(np.loadtxt(i)[:, 0])
                self.y_arr.append(np.loadtxt(i)[:, 1])
            self.fig = Figure(figsize=(3, 3))
            self.ax = self.fig.add_subplot()
            for i in range(len(self.x_arr)):
                self.ax.plot(self.x_arr[i], self.y_arr[i])
            self.fig.tight_layout()
            disconnect_zoom = zoom_factory(self.ax)
            display(self.fig.canvas)
            pan_handler = panhandler(self.fig)
            display(self.fig.canvas)
            self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
            self.toolbar.update()
        else:
            error_box = messagebox.showerror("Error", "Click Upload button to upload files")

    def scatter_file(self):
        if len(self.filePaths) >= 1:
            # Destroy the window
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            self.num_cols = 4
            self.x_arr, self.y_arr = [], []
            for i in self.filePaths:
                self.x_arr.append(np.loadtxt(i)[:, 0])
                self.y_arr.append(np.loadtxt(i)[:, 1])
            self.fig = Figure(figsize=(3, 3))
            self.ax = self.fig.add_subplot()
            for i in range(len(self.x_arr)):
                self.ax.scatter(self.x_arr[i], self.y_arr[i])
            self.fig.tight_layout()
            disconnect_zoom = zoom_factory(self.ax)
            display(self.fig.canvas)
            pan_handler = panhandler(self.fig)
            display(self.fig.canvas)
            self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
            self.toolbar.update()
        else:
            error_box = messagebox.showerror("Error", "Click Upload button to upload files")

    def lp_file(self):
        if len(self.filePaths) >= 1:
            # Destroy the window
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            self.num_cols = 5
            self.x_arr, self.y_arr = [], []
            for i in self.filePaths:
                self.x_arr.append(np.loadtxt(i)[:, 0])
                self.y_arr.append(np.loadtxt(i)[:, 1])
            self.fig = Figure(figsize=(3, 3))
            self.ax = self.fig.add_subplot()
            for i in range(len(self.x_arr)):
                self.ax.plot(self.x_arr[i], self.y_arr[i], '-o')
            self.fig.tight_layout()
            disconnect_zoom = zoom_factory(self.ax)
            display(self.fig.canvas)
            pan_handler = panhandler(self.fig)
            display(self.fig.canvas)
            self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
            self.toolbar.update()
        else:
            error_box = messagebox.showerror("Error", "Click Upload button to upload files")

    def plot3d(self):
        if len(self.filePaths) >= 1:
            # Destroy the window
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            self.num_cols = 3
            self.x_arr, self.y_arr, self.z_arr = [], [], []
            for i in self.filePaths:
                self.x_arr.append(np.loadtxt(i)[:, 0])
                self.y_arr.append(np.loadtxt(i)[:, 1])
                self.z_arr.append(np.loadtxt(i)[:, 2])
            self.fig = Figure(figsize=(3, 3))
            self.ax = self.fig.add_subplot(projection ='3d')
            for i in range(len(self.x_arr)):
                self.ax.plot3D(self.x_arr[i], self.y_arr[i], self.z_arr[i])
            self.fig.tight_layout()
            disconnect_zoom = zoom_factory(self.ax)
            display(self.fig.canvas)
            pan_handler = panhandler(self.fig)
            display(self.fig.canvas)
            self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
            self.toolbar.update()
        else:
            error_box = messagebox.showerror("Error", "Click Upload button to upload files")

    def hist_file(self):
        if len(self.filePaths) >= 1:
            # Destroy the window
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            self.num_cols = 1
            self.bin_var.set(int(self.bin_entry.get()))
            self.range_var_low.set(int(self.range_entry_low.get()))
            self.range_var_high.set(int(self.range_entry_high.get()))
            self.density_var.set(str(self.density_entry.get()))
            self.width_var.set(int(self.width_entry.get()))
            self.color_var.set(str(self.color_entry.get()))
            self.x_arr = []
            for i in self.filePaths:
                self.x_arr.append(np.loadtxt(i)[:, 0])

            self.fig = Figure(figsize=(3, 3))
            self.hist_plot()
            self.fig.tight_layout()
            disconnect_zoom = zoom_factory(self.ax)
            display(self.fig.canvas)
            pan_handler = panhandler(self.fig)
            display(self.fig.canvas)
            self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
            self.toolbar.update()
            # Destroy entries
            self.bin_lbl.destroy()
            self.range_lbl.destroy()
            self.density_lbl.destroy()
            self.width_lbl.destroy()
            self.color_lbl.destroy()
            self.bin_entry.destroy()
            self.range_entry_low.destroy()
            self.range_entry_high.destroy()
            self.density_entry.destroy()
            self.width_entry.destroy()
            self.color_entry.destroy()
        else:
            error_box = messagebox.showerror("Error", "Click Upload button to upload files")

    def back_to_hist_file(self):
        self.x_arr = []
        for i in self.filePaths:
            self.x_arr.append(np.loadtxt(i)[:, 0])

        self.fig = Figure(figsize=(3, 3))
        self.hist_plot()
        self.fig.tight_layout()
        disconnect_zoom = zoom_factory(self.ax)
        display(self.fig.canvas)
        pan_handler = panhandler(self.fig)
        display(self.fig.canvas)
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
        self.toolbar.update()

    def colorbar_file(self):
        if len(self.filePaths) >= 1:
            self.num_cols = 2.5
            # Destroy the window
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            # Set global variables
            self.colormap_name.set(str(self.colormap_entry.get()))
            self.colorbar_req.set(str(self.colorbar_entry.get()))
            self.widthbar.set(int(self.widthbar_entry.get()))
            self.lgd_string.set(str(self.lgd_string_entry.get()))
            self.colorbar_label.set(int(self.colorbar_label_entry.get()))
            self.x_arr, self.y_arr, self.z_arr = [], [], []
            for i in self.filePaths:
                self.x_arr.append(np.loadtxt(i)[:, 0])
                self.y_arr.append(np.loadtxt(i)[:, 1])
                self.z_arr.append(np.loadtxt(i)[:, 2])
            self.X = np.array(self.x_arr)
            self.Y = np.array(self.y_arr)
            self.Z = np.array(self.z_arr)
            self.fig = plt.figure(figsize=(3, 3))
            self.colorbar_plot()
            self.fig.tight_layout()
            disconnect_zoom = zoom_factory(self.ax)
            display(self.fig.canvas)
            pan_handler = panhandler(self.fig)
            display(self.fig.canvas)
            self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
            self.toolbar.update()
            # Destroy entries
            self.colormap_entry.destroy()
            self.colorbar_entry.destroy()
            self.widthbar_entry.destroy()
            self.lgd_string_entry.destroy()
            self.colorbar_label_entry.destroy()
            self.colormap_lbl.destroy()
            self.colorbar_lbl.destroy()
            self.widthbar_lbl.destroy()
            self.lgd_string_lbl.destroy()
            self.colorbar_label_lbl.destroy()
        else:
            error_box = messagebox.showerror("Error", "Click Upload button to upload files")

    def back_to_colorbar_file(self):
        self.x_arr, self.y_arr, self.z_arr = [], [], []
        for i in self.filePaths:
            self.x_arr.append(np.loadtxt(i)[:, 0])
            self.y_arr.append(np.loadtxt(i)[:, 1])
            self.z_arr.append(np.loadtxt(i)[:, 2])
        self.X = np.array(self.x_arr)
        self.Y = np.array(self.y_arr)
        self.Z = np.array(self.z_arr)
        self.fig = plt.figure(figsize=(3, 3))
        self.colorbar_plot()
        self.fig.tight_layout()
        disconnect_zoom = zoom_factory(self.ax)
        display(self.fig.canvas)
        pan_handler = panhandler(self.fig)
        display(self.fig.canvas)
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
        self.toolbar.update()

    def d3_plot(self):
        self.ax = self.fig.add_subplot(projection ='3d')
        if len(self.x_arr) == len(self.y_arr) == len(self.z_arr):
            for i in range(len(self.x_arr)):
                if self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() != 0:
                    self.ax.plot3D(self.x_arr[i], self.y_arr[i], self.z_arr[i], c=self.new_var_arr[i].get(), label=self.legend_var_arr[i].get())
                    self.ax.set_legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() != 0:
                    self.ax.plot3D(self.x_arr[i], self.y_arr[i], self.z_arr[i], c=self.new_var_arr[i].get())
                elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() == 0:
                    self.ax.plot3D(self.x_arr[i], self.y_arr[i], self.z_arr[i], label=self.legend_var_arr[i].get())
                    self.ax.set_legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                else:
                    self.ax.plot3D(self.x_arr[i], self.y_arr[i], self.z_arr[i])

    def line_plot(self):
        self.ax = self.fig.add_subplot()
        if len(self.x_arr) == len(self.y_arr):
            for i in range(len(self.x_arr)):
                if self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() != 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() != 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get())
                elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() == 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                else:
                    self.ax.plot(self.x_arr[i], self.y_arr[i])

    def scatter_plot(self):
        self.ax = self.fig.add_subplot()
        if len(self.x_arr) == len(self.y_arr):
            for i in range(len(self.x_arr)):
                if self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() != 0:
                    self.ax.scatter(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() != 0:
                    self.ax.scatter(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get())
                elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() == 0:
                    self.ax.scatter(self.x_arr[i], self.y_arr[i], label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                else:
                    self.ax.scatter(self.x_arr[i], self.y_arr[i])

    def lp_plot(self):
        self.ax = self.fig.add_subplot()
        if len(self.x_arr) == len(self.y_arr):
            for i in range(len(self.x_arr)):
                if self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() != 0 and self.marker_var_arr[i].get() != 0 and self.marker_size_var_arr[i].get() != 0 and self.linewidth_var_arr[i].get() != 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), marker=self.marker_var_arr[i].get(), markersize=self.marker_size_var_arr[i].get(), linewidth=self.linewidth_var_arr[i].get(), label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() != 0 and self.marker_var_arr[i].get() != 0 and self.marker_size_var_arr[i].get() != 0 and self.linewidth_var_arr[i].get() != 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), marker=self.marker_var_arr[i].get(), markersize=self.marker_size_var_arr[i].get(), linewidth=self.linewidth_var_arr[i].get())
                elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() == 0 and self.marker_var_arr[i].get() != 0 and self.marker_size_var_arr[i].get() != 0 and self.linewidth_var_arr[i].get() != 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], marker=self.marker_var_arr[i].get(), markersize=self.marker_size_var_arr[i].get(), linewidth=self.linewidth_var_arr[i].get(), label=self.legend_var_arr[i].get())
                elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() == 0 and self.marker_var_arr[i].get() != 0 and self.marker_size_var_arr[i].get() != 0 and self.linewidth_var_arr[i].get() != 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], marker=self.marker_var_arr[i].get(), markersize=self.marker_size_var_arr[i].get(), linewidth=self.linewidth_var_arr[i].get())
                elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() != 0 and self.marker_var_arr[i].get() == 0 and self.marker_size_var_arr[i].get() == 0 and self.linewidth_var_arr[i].get() == 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), marker='o', markersize=5, label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() != 0 and self.marker_var_arr[i].get() == 0 and self.marker_size_var_arr[i].get() == 0 and self.linewidth_var_arr[i].get() == 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), marker='o', markersize=5)
                elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() == 0 and self.marker_var_arr[i].get() == 0 and self.marker_size_var_arr[i].get() == 0 and self.linewidth_var_arr[i].get() == 0:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], marker='o', markersize=5, label=self.legend_var_arr[i].get())
                    self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
                else:
                    self.ax.plot(self.x_arr[i], self.y_arr[i], '-o')

    def hist_plot(self):
        self.ax = self.fig.add_subplot()
        self.xx, self.yy = [], []
        for i in range(len(self.x_arr)):
            hist, edges = np.histogram(self.x_arr[i], int(self.bin_var.get()), range=(self.range_var_low.get(), self.range_var_high.get()), density=self.density_var.get())
            self.yy.append(hist.round(3).tolist())
            self.xx.append(edges[:-1].round(3).tolist())

        for i in range(len(self.filePaths)):
            if self.new_var_arr[i].get() == 0:
                for i in range(len(self.xx)):
                    self.ax.bar(self.xx[i], self.yy[i], width=self.width_var.get(), color=self.color_var.get())
            elif self.new_var_arr[i].get() != 0:
                for i in range(len(self.xx)):
                    self.ax.bar(self.xx[i], self.yy[i], width=self.width_var.get(), color=self.new_var_arr[i].get())

    def colorbar_plot(self):
        self.ax = self.fig.add_subplot()
        for i in range(len(self.X)):
            colors = self.Z[i][:]
            norm = Normalize(vmin=0, vmax=1)
            color_arr = norm(colors)
            cm = plt.cm.get_cmap(self.colormap_name.get())
            if self.legend_var_arr[i].get() != 0 and self.widthbar.get() != 0:
                sc = self.ax.bar(self.X[i], self.Y[i], width=self.widthbar.get(), color=cm(color_arr), label=self.legend_var_arr[i].get())
                self.ax.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
            elif self.widthbar.get() != 0 and self.legend_var_arr[i].get() == 0:
                sc = self.ax.bar(self.X[i], self.Y[i], width=self.widthbar.get(), color=cm(color_arr))
            else:
                sc = self.ax.bar(self.X[i], self.Y[i], color=cm(color_arr))
            sm = ScalarMappable(cmap=cm, norm=norm)
            sm.set_array([])
            if self.colorbar_req.get() == 'True':
                st = self.lgd_string.get()   # Add 'r' for scientific symbol from latex
                cbar = self.fig.colorbar(sm, label=st)
                cbar.ax.tick_params(labelsize=self.colorbar_label.get())

    def module_plot(self):
        self.canvas.get_tk_widget().destroy() 
        self.toolbar.destroy()  
        if self.xFig.get() != 0 and self.yFig.get() != 0 :
            self.fig = Figure(figsize=(self.xFig.get(), self.yFig.get()))
        else:
            self.fig = Figure(figsize=(3, 3))
        # Line plot
        if self.num_cols == 1:
            self.hist_plot()
        elif self.num_cols == 2:
            self.line_plot()
        elif self.num_cols == 2.5:
            self.colorbar_plot()
        elif self.num_cols == 3:
            self.d3_plot()
        elif self.num_cols == 4:
            self.scatter_plot()
        elif self.num_cols == 5:
            self.lp_plot()

        if self.num_cols != 3:
            if self.xLabel.get() != 0 and self.yLabel.get() != 0:
                self.ax.set_xlabel(self.xLabel.get(), fontsize=self.tkFont.get())
                self.ax.set_ylabel(self.yLabel.get(), fontsize=self.tkFont.get())
        elif self.num_cols == 3:
            if self.xLabel.get() != 0 and self.yLabel.get() != 0 and self.zLabel.get() != 0:
                self.ax.set_xlabel(self.xLabel.get(), fontsize=self.tkFont.get())
                self.ax.set_ylabel(self.yLabel.get(), fontsize=self.tkFont.get())
                self.ax.set_zlabel(self.zLabel.get(), fontsize=self.tkFont.get())

        if self.num_cols != 3:
            if self.xLower.get() != 0 and self.xUpper.get() != 0:
                self.ax.set_xlim(self.xLower.get(), self.xUpper.get())
            if self.yLower.get() != 0 and self.yUpper.get() != 0:
                self.ax.set_ylim(self.yLower.get(), self.yUpper.get())
            if self.xLower.get() != 0 or self.xUpper.get() != 0:
                self.ax.set_xlim(self.xLower.get(), self.xUpper.get())
            if self.yLower.get() != 0 or self.yUpper.get() != 0:
                self.ax.set_ylim(self.yLower.get(), self.yUpper.get())
        elif self.num_cols == 3:
            if self.xLower.get() != 0 and self.xUpper.get() != 0:
                self.ax.set_xlim(self.xLower.get(), self.xUpper.get())
            if self.yLower.get() != 0 and self.yUpper.get() != 0:
                self.ax.set_ylim(self.yLower.get(), self.yUpper.get())
            if self.zLower.get() != 0 and self.zUpper.get() != 0:
                self.ax.set_zlim(self.zLower.get(), self.zUpper.get())

        if self.num_cols != 3 and self.num_cols != 1:
            if self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() != 0 and self.yLower.get() != 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
            
            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() == 0 and self.xUpper.get() != 0 and self.yLower.get() != 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() == 0 and self.yLower.get() != 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() != 0 and self.yLower.get() == 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() != 0 and self.yLower.get() != 0 and self.yUpper.get() == 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() == 0 and self.xUpper.get() != 0 and self.yLower.get() == 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() == 0 and self.yLower.get() != 0 and self.yUpper.get() == 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() == 0 and self.xUpper.get() == 0 and self.yLower.get() == 0 and self.yUpper.get() == 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    mix_x_arr, mix_y_arr = [], []
                    for i in range(len(self.x_arr)):
                        for j in range(len(self.x_arr[i])):
                            mix_x_arr.append(self.x_arr[i][j])
                            mix_y_arr.append(self.y_arr[i][j])

                    x_width = (np.max(mix_x_arr) - np.min(mix_x_arr))/self.tk_xbin.get()
                    y_width = (np.max(mix_y_arr) - np.min(mix_y_arr))/self.tk_ybin.get()
                    x_level = np.arange(np.min(mix_x_arr), np.max(mix_x_arr), float(x_width), dtype=float)
                    y_level = np.arange(np.min(mix_y_arr), np.max(mix_y_arr), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

        if self.num_cols != 3 and self.num_cols == 1:
            if self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() != 0 and self.yLower.get() != 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() == 0 and self.xUpper.get() != 0 and self.yLower.get() != 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() == 0 and self.yLower.get() != 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() != 0 and self.yLower.get() == 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() != 0 and self.yLower.get() != 0 and self.yUpper.get() == 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() == 0 and self.xUpper.get() != 0 and self.yLower.get() == 0 and self.yUpper.get() != 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() != 0 and self.xUpper.get() == 0 and self.yLower.get() != 0 and self.yUpper.get() == 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    x_width = (self.xUpper.get() - self.xLower.get())/self.tk_xbin.get()
                    y_width = (self.yUpper.get() - self.yLower.get())/self.tk_ybin.get()
                    x_level = np.arange(float(self.xLower.get()), float(self.xUpper.get()), float(x_width), dtype=float)
                    y_level = np.arange(float(self.yLower.get()), float(self.yUpper.get()), float(y_width), dtype=float)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get()) 
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

            elif self.xy_ticks.get() !=0 and self.tk_len.get() != 0 and self.xLower.get() == 0 and self.xUpper.get() == 0 and self.yLower.get() == 0 and self.yUpper.get() == 0:
                if self.tk_xbin.get() != 0 and self.tk_ybin.get() != 0:
                    mix_x_arr, mix_y_arr = [], []
                    for i in range(len(self.xx)):
                        for j in range(len(self.xx[i])):
                            mix_x_arr.append(self.xx[i][j])
                            mix_y_arr.append(self.yy[i][j])

                    x_width = (np.max(mix_x_arr) - np.min(mix_x_arr))/self.tk_xbin.get()
                    y_width = (np.max(mix_y_arr) - 0.0)/self.tk_ybin.get()
                    x_level = np.arange(np.min(mix_x_arr), np.max(mix_x_arr), float(x_width), dtype=float)
                    y_level = np.arange(0.0, np.max(mix_y_arr), float(y_width), dtype=float)
                    x_level = x_level.round(0)
                    if self.density_var.get() == 'True':
                        y_level = y_level.round(3)
                    else:
                        y_level = y_level.round(0)
                    self.ax.set_xticks(x_level)
                    self.ax.set_yticks(y_level)
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())
                else:
                    self.ax.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get(), labelsize=self.tkFont.get())

        self.fig.tight_layout()
        disconnect_zoom = zoom_factory(self.ax)
        display(self.fig.canvas)
        pan_handler = panhandler(self.fig)
        display(self.fig.canvas)
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        self.toolbar.update()

    def plot_file_labeling(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        x_label = str(self.xlabel.get())
        y_label = str(self.ylabel.get())
        self.xLabel.set(x_label)
        self.yLabel.set(y_label)
        if self.num_cols == 3:
            z_label = str(self.zlabel.get())
            self.zLabel.set(z_label)
        self.tkFont.set(int(self.xyticks_font.get()))
        self.module_plot()
        # Destroy the previous entries
        self.xlabel.destroy()
        self.ylabel.destroy()
        self.xlbl.destroy()
        self.ylbl.destroy()
        self.xlbl_opt.destroy()
        self.ylbl_opt.destroy()
        if self.num_cols == 3:
            self.zlabel.destroy()
            self.zlbl.destroy()
            self.zlbl_opt.destroy()
        self.xyticks_font_label.destroy()
        self.xyticks_font.destroy()
        self.font_opt.destroy()

    def plot_file_range(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        # Get the range of x and y
        x_range_lower = float(self.xrange_lower.get())
        x_range_upper = float(self.xrange_upper.get())
        y_range_lower = float(self.yrange_lower.get())
        y_range_upper = float(self.yrange_upper.get())
        y_range_lower = float(self.yrange_lower.get())
        y_range_upper = float(self.yrange_upper.get())
        # Set the x, y range for later use
        self.xLower.set(x_range_lower)
        self.xUpper.set(x_range_upper)
        self.yLower.set(y_range_lower)
        self.yUpper.set(y_range_upper)
        if self.num_cols == 3:
            z_range_lower = float(self.zrange_lower.get())
            z_range_upper = float(self.zrange_upper.get())
            self.zLower.set(z_range_lower)
            self.zUpper.set(z_range_upper)
        # Plot
        self.module_plot()
        # Destroy the previous entries
        self.xrange_lower.destroy()
        self.xrange_upper.destroy()
        self.yrange_lower.destroy()
        self.yrange_upper.destroy()
        self.xlim_lower.destroy()
        self.xlim_upper.destroy()
        self.ylim_lower.destroy()
        self.ylim_upper.destroy()
        self.xlim_lower_opt.destroy()
        self.xlim_upper_opt.destroy()
        self.ylim_lower_opt.destroy()
        self.ylim_upper_opt.destroy()
        if self.num_cols == 3:
            self.zlim_lower.destroy()
            self.zlim_upper.destroy()
            self.zrange_lower.destroy()
            self.zrange_upper.destroy()
            self.zlim_lower_opt.destroy()
            self.zlim_upper_opt.destroy()

    def plot_figsize(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        # Get the figsize 
        x_fig = int(self.xfig.get())
        y_fig = int(self.yfig.get())
        # Set the x, y fig dimension for later use
        self.xFig.set(x_fig)
        self.yFig.set(y_fig)
        # Plot
        self.module_plot()
        # Destroy the previous entries
        self.xyfig.destroy()
        self.xfig.destroy()
        self.yfig.destroy()
        self.xyfig_opt.destroy()

    def plot_xyticks(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        # Get the ticks info
        self.xy_ticks.set(str(self.xy.get()))
        self.tk_len.set(float(self.xyticks_len.get()))
        self.tkFont.set(float(self.xyticks_font.get()))
        self.tk_xbin.set(int(self.xbin.get()))
        self.tk_ybin.set(int(self.ybin.get()))
        if self.num_cols == 3:
            self.tk_zbin.set(int(self.zbin.get()))
        # Plot
        self.module_plot()
        # Destroy the previous entries
        self.xyticks_label.destroy()
        self.xyticks_len_label.destroy()
        self.xyticks_in.destroy()
        self.xyticks_out.destroy()
        self.xyticks_len.destroy()
        self.xyticks_font_label.destroy()
        self.xyticks_font.destroy()
        self.xyticks_font_label.destroy()
        self.xbin_label.destroy()
        self.xbin.destroy()
        self.ybin_label.destroy()
        self.ybin.destroy()
        self.xyticks_len_opt.destroy()
        self.xyticks_font_opt.destroy()
        self.xbin_opt.destroy()
        self.ybin_opt.destroy()

    def plot_color(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        self.new_var_arr = []
        for i in range(len(self.filePaths)):
            new_var = 'entry_' + str(i)
            self.new_var = StringVar()
            self.new_var.set(str(self.variables_arr[i].get()))
            self.new_var_arr.append(self.new_var)

        # Plot
        self.module_plot()
        # Destroy
        self.color_lbl.destroy()
        for i in range(len(self.x_arr)):
            self.variables_arr[i].destroy()
        self.color_opt.destroy()

    def plot_legend(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        self.legend_var_arr = []
        for i in range(len(self.x_arr)):
            legend_var = 'entry_' + str(i)
            self.legend_var = StringVar()
            self.legend_var.set(str(self.legend_arr[i].get()))
            self.legend_var_arr.append(self.legend_var)
        self.lgdFont.set(int(self.lgd_font.get()))
        self.lgdLoc.set(str(self.lgd_loc.get()))
        # Plot
        self.module_plot()
        # Destroy entries
        self.legend_lbl.destroy()
        for i in range(len(self.x_arr)):
            self.legend_arr[i].destroy()
        self.legend_font.destroy()
        self.lgd_font.destroy()
        self.legend_location.destroy()
        self.lgd_loc.destroy()

    def plot_lp(self):
        # Destroy the window
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        # Get the entries
        self.marker_var_arr, self.marker_size_var_arr, self.linewidth_var_arr = [], [], []
        for i in range(len(self.filePaths)):
            marker_var = 'marker' + str(i)
            marker_size_var = 'marker_size' + str(i)
            linewidth_var = 'linewidth' + str(i)
            self.marker_var = StringVar()
            self.marker_size_var = IntVar()
            self.linewidth_var = IntVar()
            self.marker_var.set(str(self.marker_variable_arr[i].get()))
            self.marker_size_var.set(int(self.marker_size_variable_arr[i].get()))
            self.linewidth_var.set(int(self.linewidth_variable_arr[i].get()))
            self.marker_var_arr.append(self.marker_var)
            self.marker_size_var_arr.append(self.marker_size_var)
            self.linewidth_var_arr.append(self.linewidth_var)

        # Plot
        self.module_plot()
        # Destroy all entries
        self.marker_lbl.destroy()
        self.marker_size_lbl.destroy()
        self.linewidth_lbl.destroy()
        for i in range(len(self.filePaths)):
            self.marker_variable_arr[i].destroy()
            self.marker_size_variable_arr[i].destroy()
            self.linewidth_variable_arr[i].destroy()

    def set_xylabel(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                self.xlbl = Label(window, text="x-label", bg="white")
                self.xlabel = Entry(window, width=7)
                self.xlbl_opt = Label(window, text="(Str)", bg="white")
                self.xlbl.place(x=5, y=380)
                self.xlabel.place(x=60, y=380)
                self.xlbl_opt.place(x=130, y=380)
                self.ylbl = Label(window, text="y-label", bg="white")
                self.ylabel = Entry(window, width=7)
                self.ylbl.place(x=5, y=410)
                self.ylabel.place(x=60, y=410)
                self.ylbl_opt = Label(window, text="(Str)", bg="white")
                self.ylbl_opt.place(x=130, y=410)
                j = 30
                if self.num_cols == 3:
                    self.zlbl = Label(window, text="z-label", bg="white")
                    self.zlabel = Entry(window, width=7)
                    self.zlbl.place(x=5, y=410+j)
                    self.zlabel.place(x=60, y=410+j)
                    self.zlbl_opt = Label(window, text="(Str)", bg="white")
                    self.zlbl_opt.place(x=130, y=410+j)
                    j = j + 30

                self.xyticks_font_label = Label(window, text="Fontsize", bg="white")
                self.xyticks_font = Entry(window, width=5)
                self.xyticks_font_label.place(x=5, y=410+j)
                self.xyticks_font.place(x=70, y=410+j)
                self.font_opt = Label(window, text="(Int)", bg="white")
                self.font_opt.place(x=130, y=410+j)
                btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_file_labeling())
                btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")

    def set_lp(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                self.marker_lbl = Label(window, text="Marker", bg="white")
                self.marker_size_lbl = Label(window, text="Marker size", bg="white")
                self.linewidth_lbl = Label(window, text="Linewidth", bg="white")
                self.marker_lbl.place(x=5, y=380)
                self.marker_size_lbl.place(x=5, y=410)
                self.linewidth_lbl.place(x=5, y=440)
                j = 0
                self.marker_variable_arr, self.marker_size_variable_arr, self.linewidth_variable_arr =[], [], []
                for i in range(len(self.filePaths)):
                    marker_variable = 'marker' + str(i)
                    marker_size_variable = 'marker_size' + str(i)
                    linewidth_variable = 'linewidth' + str(i)
                    self.marker_variable = Entry(window, width=3)
                    self.marker_size_variable = Entry(window, width=3)
                    self.linewidth_variable = Entry(window, width=3)
                    self.marker_variable.place(x=80+j, y=380)
                    self.marker_size_variable.place(x=100+j, y=410)
                    self.linewidth_variable.place(x=90+j, y=440)
                    self.marker_variable_arr.append(self.marker_variable)
                    self.marker_size_variable_arr.append(self.marker_size_variable)
                    self.linewidth_variable_arr.append(self.linewidth_variable)
                    j = j+50

                btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_lp())
                btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")

    def set_xyrange(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                # Entries  
                self.xlim_lower = Label(window, text="xlim-L", bg="white")
                self.xlim_upper = Label(window, text="xlim-U", bg="white")
                self.ylim_lower = Label(window, text="ylim-L", bg="white")
                self.ylim_upper = Label(window, text="ylim-U", bg="white")
                self.xlim_lower_opt = Label(window, text="(Int/Double)", bg="white")
                self.xlim_upper_opt = Label(window, text="(Int/Double)", bg="white")
                self.ylim_lower_opt = Label(window, text="(Int/Double)", bg="white")
                self.ylim_upper_opt = Label(window, text="(Int/Double)", bg="white")
                self.xrange_lower = Entry(window, width=5)
                self.xrange_upper = Entry(window, width=5)
                self.yrange_lower = Entry(window, width=5)
                self.yrange_upper = Entry(window, width=5)
                self.xlim_lower.place(x=5, y=380)
                self.xrange_lower.place(x=60, y=380)
                self.xlim_upper.place(x=5, y=410)
                self.xrange_upper.place(x=60, y=410)
                self.ylim_lower.place(x=5, y=440)
                self.yrange_lower.place(x=60, y=440)
                self.ylim_upper.place(x=5, y=470)
                self.yrange_upper.place(x=60, y=470)
                self.xlim_lower_opt.place(x=130, y=380)
                self.xlim_upper_opt.place(x=130, y=410)
                self.ylim_lower_opt.place(x=130, y=440)
                self.ylim_upper_opt.place(x=130, y=470)
                j = 30
                if self.num_cols == 3:
                    self.zlim_lower = Label(window, text="zlim-L", bg="white")
                    self.zlim_upper = Label(window, text="zlim-U", bg="white")
                    self.zlim_lower_opt = Label(window, text="(Int/double)", bg="white")
                    self.zlim_upper_opt = Label(window, text="(Int/double)", bg="white")
                    self.zrange_lower = Entry(window, width=5)
                    self.zrange_upper = Entry(window, width=5)
                    self.zlim_lower.place(x=5, y=470+j)
                    self.zrange_lower.place(x=60, y=470+j)
                    self.zlim_upper.place(x=5, y=470+2*j)
                    self.zrange_upper.place(x=60, y=470+2*j)
                    self.zlim_lower_opt.place(x=130, y=470+j)
                    self.zlim_upper_opt.place(x=130, y=470+2*j)

                btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_file_range())
                btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")

    def set_figsize(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                # Entries
                self.xyfig = Label(window, text="Fig dim", bg="white")
                self.xyfig_opt = Label(window, text="(Int/Double)", bg="white")
                self.xfig = Entry(window, width=3)
                self.yfig = Entry(window, width=3)
                self.xyfig.place(x=5, y=380)
                self.xfig.place(x=60, y=380)
                self.yfig.place(x=100, y=380)
                self.xyfig_opt.place(x=5, y=420)

                # Replot button
                btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_figsize())
                btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")

    def get_ticks_in(self):
        self.xy.set(str('in'))
    
    def get_ticks_out(self):
        self.xy.set(str('out'))

    def set_xyticks(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                if self.num_cols != 3:
                    v0=IntVar()
                    v0.set(1)
                    self.xyticks_label = Label(window, text="xy-ticks", bg="white")
                    self.xyticks_in=Radiobutton(window, text="in", variable=v0, value=1, bg="white", command=lambda: self.get_ticks_in())
                    self.xyticks_out=Radiobutton(window, text="out", variable=v0, value=0, bg="white", command=lambda: self.get_ticks_out())
                    self.xyticks_len_label = Label(window, text="Tick length", bg="white")
                    self.xyticks_len_opt = Label(window, text="(Int/Double)", bg="white")
                    self.xyticks_len = Entry(window, width=5)
                    self.xyticks_font_label = Label(window, text="Fontsize", bg="white")
                    self.xyticks_font_opt = Label(window, text="(Int/Double)", bg="white")
                    self.xyticks_font = Entry(window, width=5)
                    self.xbin_label = Label(window, text="x-bin", bg="white")
                    self.ybin_label = Label(window, text="y-bin", bg="white")
                    self.xbin_opt = Label(window, text="(Int)", bg="white")
                    self.ybin_opt = Label(window, text="(Int)", bg="white")
                    self.xbin = Entry(window, width=5)
                    self.ybin = Entry(window, width=5)
                    # Set positions
                    self.xyticks_label.place(x=5, y=380)
                    self.xyticks_len_label.place(x=5, y=410)
                    self.xyticks_in.place(x=60, y=380)
                    self.xyticks_out.place(x=110, y=380)
                    self.xyticks_len.place(x=90, y=410)
                    self.xyticks_font_label.place(x=5, y=450)
                    self.xyticks_font.place(x=90, y=450)
                    self.xbin_label.place(x=5, y=480)
                    self.ybin_label.place(x=5, y=510)
                    self.xbin.place(x=90, y=480)
                    self.ybin.place(x=90, y=510)
                    self.xyticks_len_opt.place(x=140, y=410)
                    self.xyticks_font_opt.place(x=140, y=450)
                    self.xbin_opt.place(x=140, y=480)
                    self.ybin_opt.place(x=140, y=510)
                    j = 30

                    # Replot button
                    btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_xyticks())
                    btn_replot.place(x=72, y=5)
                else:
                    btn_replot = Button(window, text="Replot", height=1, width=5)
                    btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")

    def set_color(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                # Set butoon and entries
                self.color_lbl = Label(window, text="Set color", bg="white")
                j = 0
                self.variables_arr = []
                for i in range(len(self.filePaths)):
                    variable = 'color_entry_' + str(i)
                    self.variable = Entry(window, width=7)
                    self.variable.place(x=5, y=410+j)
                    self.variables_arr.append(self.variable)
                    j = j + 30

                self.color_lbl.place(x=5, y=380)
                self.color_opt = Label(window, text="(String)", bg="white")
                self.color_opt.place(x=5, y=410+j)
                # Replot button
                btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_color())
                btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")

    def set_legend(self):
        if len(self.filePaths) >= 1:
            if len(self.x_arr) > 0 and len(self.y_arr) > 0:
                # Set butoon and entries
                self.legend_lbl = Label(window, text="Set legend", bg="white")
                self.legend_arr = []
                j = 0
                for i in range(len(self.filePaths)):
                    lgd = 'legend_entry_' + str(i)
                    self.lgd = Entry(window, width=10)
                    self.lgd.place(x=5, y=410+j)
                    self.legend_arr.append(self.lgd)
                    j = j + 30

                self.legend_lbl.place(x=5, y=380)
                self.legend_font = Label(window, text="Fontsize", bg="white")
                self.legend_font.place(x=5, y=410+j)
                self.lgd_font = Entry(window, width=5)
                self.lgd_font.place(x=70, y=410+j)
                self.legend_location = Label(window, text="Location", bg="white")
                self.legend_location.place(x=5, y=410+j+30)
                self.lgd_loc = Entry(window, width=5)
                self.lgd_loc.place(x=70, y=410+j+30)
                # Replot button
                btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_legend())
                btn_replot.place(x=72, y=5)
            else:
                error_box = messagebox.showerror("Instructions", "Please do any kind of plot")
        else:
            error_box = messagebox.showerror("Instructions", "Please upload any file")


    def set_hist(self):
        if len(self.filePaths) >= 1:
            self.bin_lbl = Label(window, text="Set bin", bg="white")
            self.range_lbl = Label(window, text="Set range", bg="white")
            self.density_lbl = Label(window, text="Set density", bg="white")
            self.width_lbl = Label(window, text="Set bar width", bg="white")
            self.color_lbl = Label(window, text="Set color", bg="white")
            self.bin_lbl.place(x=5, y=380)
            self.range_lbl.place(x=5, y=420)
            self.density_lbl.place(x=5, y=460)
            self.width_lbl.place(x=5, y=500)
            self.color_lbl.place(x=5, y=540)
            # Entries
            self.bin_entry = Entry(window, width=7)
            self.range_entry_low = Entry(window, width=5)
            self.range_entry_high = Entry(window, width=5)
            self.density_entry = Entry(window, width=10)
            self.width_entry = Entry(window, width=5)
            self.color_entry = Entry(window, width=10)
            self.bin_entry.place(x=90, y=380)
            self.range_entry_low.place(x=90, y= 420)
            self.range_entry_high.place(x=150, y= 420)
            self.density_entry.place(x=90, y=460)
            self.width_entry.place(x=90, y=500)
            self.color_entry.place(x=90, y=540)
            # Replot button
            btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.hist_file())
            btn_replot.place(x=72, y=5)
        else:
            error_box = messagebox.showerror("Instructions", "Please do any kind of plot")

    def set_colorbar(self):
        if len(self.filePaths) >= 1:
            self.colormap_lbl = Label(window, text="Set colormap", bg="white")
            self.colormap_entry = Entry(window, width=10)
            self.colormap_lbl.place(x=5, y=380)
            self.colormap_entry.place(x=100, y=380)
            self.colorbar_lbl = Label(window, text="Set colorbar", bg="white")
            self.colorbar_entry = Entry(window, width=10)
            self.colorbar_lbl.place(x=5, y=410)
            self.colorbar_entry.place(x=100, y=410)
            self.widthbar_lbl = Label(window, text="bar width", bg="white")
            self.lgd_string_lbl = Label(window, text="z-label", bg="white")
            self.widthbar_entry = Entry(window, width=3)
            self.lgd_string_entry = Entry(window, width=10)
            self.widthbar_lbl.place(x=5, y=440)
            self.widthbar_entry.place(x=100, y=440)
            self.lgd_string_lbl.place(x=5, y=470)
            self.lgd_string_entry.place(x=100, y=470)
            self.colorbar_label_lbl = Label(window, text="Labelsize", bg="white")
            self.colorbar_label_entry = Entry(window, width=3)
            self.colorbar_label_lbl.place(x=5, y=500)
            self.colorbar_label_entry.place(x=100, y=500)
            # Replot button
            btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.colorbar_file())
            btn_replot.place(x=72, y=5)
        else:
            error_box = messagebox.showerror("Instructions", "Click Upload button to upload files")

    def set_back(self):
        if self.num_cols == 2:
            self.plot_file()
        elif self.num_cols == 1:
            self.back_to_hist_file()
        elif self.num_cols == 2.5:
            self.back_to_colorbar_file()
        elif self.num_cols == 3:
            self.plot3d()

    def save_fig(self):
        out_filename = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        filename = out_filename.name
        if not filename:
            return
        self.fig.savefig(filename, dpi=600)

window = Tk()
window.title('skPlot') 
window.geometry("800x600+10+10") 
window.configure(bg='white')

data = {}
ps = plot_save(window)

# Menubar
btn_upload = Button(window, text="Upload", height=1, width=4, command=lambda: ps.upload_file())
btn_upload.place(x=5, y=5)
btn_plot = Button(window, text="Line plot", height=1, width=5, command=lambda: ps.plot_file())
btn_plot.place(x=72, y=5)
btn_lp = Button(window, text="Line-point", height=1, width=7, command=lambda: ps.lp_file())
btn_lp.place(x=145, y=5)
btn_set_xyscatter = Button(window, text="Scatter plot", height=1, width=7, command=lambda: ps.scatter_file())
btn_set_xyscatter.place(x=235, y=5)
btn_hist = Button(window, text="Histogram plot", height=1, width=10, command=lambda: ps.set_hist())
btn_hist.place(x=325, y=5)
btn_colorbar = Button(window, text="Color z-axis", height=1, width=7, command=lambda: ps.set_colorbar())
btn_colorbar.place(x=440, y=5)
btn_3dplot = Button(window, text="3D plot", height=1, width=5, command=lambda: ps.plot3d())
btn_3dplot.place(x=530, y=5)
btn_save = Button(window, text="Save", height=1, width=3, command=lambda: ps.save_fig())
btn_save.place(x=605, y=5)

btn_set_xylabel = Button(window, text="Set label", height=1, width=7, command=lambda: ps.set_xylabel())
btn_set_xylabel.place(x=5, y=40)
btn_set_xyrange = Button(window, text="Set range", height=1, width=7, command=lambda: ps.set_xyrange())
btn_set_xyrange.place(x=95, y=40)
btn_set_xyfigsize = Button(window, text="Set figsize", height=1, width=7, command=lambda: ps.set_figsize())
btn_set_xyfigsize.place(x=185, y=40)
btn_set_xyticks = Button(window, text="Set ticks", height=1, width=7, command=lambda: ps.set_xyticks())
btn_set_xyticks.place(x=275, y=40)
btn_set_xycolor = Button(window, text="Set color", height=1, width=5, command=lambda: ps.set_color())
btn_set_xycolor.place(x=365, y=40)
btn_set_xylegend = Button(window, text="Set legend", height=1, width=7, command=lambda: ps.set_legend())
btn_set_xylegend.place(x=440, y=40)
btn_set_marker = Button(window, text="Set marker", height=1, width=7, command=lambda: ps.set_lp())
btn_set_marker.place(x=530, y=40)
input_lbl = Label(window, text="Input section", font=('Arial', 15), bg="white")
input_lbl.place(x=5, y=300)

exit_button = Button(window, text="Exit", width=3, command=lambda: window.destroy)
exit_button.place(x=330, y=500)
back_button = Button(window, text="Back", width=3, command=lambda: ps.set_back())
back_button.place(x=390, y=500)

upload_msgbox = messagebox.showinfo("Instructions", "Click Upload button to upload files")

# run the gui
window.mainloop()

