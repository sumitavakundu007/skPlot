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
        self.xFig = IntVar()
        self.yFig = IntVar()
        self.xy = StringVar()
        self.xy_ticks = StringVar()
        self.tk_len = IntVar()
        self.xyticks_len = IntVar()
        self.tkFont = IntVar()
        self.tk_xbin = IntVar()
        self.tk_ybin = IntVar()
        self.tk_zbin = IntVar()
        self.bin_var = IntVar()
        self.range_var_low = IntVar()
        self.range_var_high = IntVar()
        self.density_var = StringVar()
        self.width_var = IntVar()
        self.color_var = StringVar()
        self.num_cols = 0
        self.widthbar = IntVar()
        self.lgd_string = StringVar()
        self.colormap_name = StringVar()
        self.colorbar_req = StringVar()
        self.colorbar_label = IntVar()

    def upload_file(self):
        files = filedialog.askopenfilenames(multiple=True)
        var = window.tk.splitlist(files)
        self.filePaths = []
        for f in var:
            self.filePaths.append(f)

        self.new_var_arr = [IntVar() for i in range(len(self.filePaths))]
        self.legend_var_arr = [IntVar() for i in range(len(self.filePaths))]
        self.lgdFont = IntVar()
        self.lgdLoc = StringVar()

    def plot_file(self):
        self.num_cols = 2
        self.x_arr, self.y_arr = [], []
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
        toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        toolbar.update()

    def plot3d(self):
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
        toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        toolbar.update()

    def hist_file(self):
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
        toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        toolbar.update()
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
        toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
        toolbar.update()

    def colorbar_file(self):
        self.num_cols = 2.5
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
        toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=True)
        toolbar.update()
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
        toolbar = NavigationToolbar2Tk(self.canvas, window, pack_toolbar=False)
        toolbar.update()

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

    def hist_plot(self):
        self.ax = self.fig.add_subplot()
        for i in range(len(self.x_arr)):
            # if self.range_var_low.get() != 0 and self.range_var_high.get() != 0 and  self.density_var.get() != 0 and self.width_var.get() != 0 and self.color_var.get() != 0:
            self.ax.hist(self.x_arr[i], self.bin_var.get(), range=(self.range_var_low.get(), self.range_var_high.get()), density=self.density_var.get(), width=self.width_var.get(), color=self.color_var.get())

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
        elif self.num_cols == 3:
            if self.xLower.get() != 0 and self.xUpper.get() != 0:
                self.ax.set_xlim(self.xLower.get(), self.xUpper.get())
            if self.yLower.get() != 0 and self.yUpper.get() != 0:
                self.ax.set_ylim(self.yLower.get(), self.yUpper.get())
            if self.zLower.get() != 0 and self.zUpper.get() != 0:
                self.ax.set_zlim(self.zLower.get(), self.zUpper.get())

        if self.num_cols != 3:
            if self.xy_ticks.get() !=0 and self.tk_len.get() != 0:
                plt.xticks(fontsize=self.tkFont.get())
                plt.yticks(fontsize=self.tkFont.get())
                plt.locator_params(axis='x', nbins=self.tk_xbin.get())
                plt.locator_params(axis='y', nbins=self.tk_ybin.get())
                plt.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get())       

        self.fig.tight_layout()
        disconnect_zoom = zoom_factory(self.ax)
        display(self.fig.canvas)
        pan_handler = panhandler(self.fig)
        display(self.fig.canvas)
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=RIGHT, expand=1)

    def plot_scatter(self):
        if self.xFig.get() != 0 and self.yFig.get() != 0 :
            self.fig = plt.figure(figsize=(self.xFig.get(), self.yFig.get()))
        else:
            self.fig = plt.figure(figsize=(3, 3))
        for i in range(len(self.x_arr)):
            if self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() != 0:
                plt.scatter(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get(), label=self.legend_var_arr[i].get())
                plt.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
            elif self.legend_var_arr[i].get() == 0 and self.new_var_arr[i].get() != 0:
                plt.scatter(self.x_arr[i], self.y_arr[i], c=self.new_var_arr[i].get())
            elif self.legend_var_arr[i].get() != 0 and self.new_var_arr[i].get() == 0:
                plt.scatter(self.x_arr[i], self.y_arr[i], label=self.legend_var_arr[i].get())
                plt.legend(fontsize=self.lgdFont.get(), loc=str(self.lgdLoc.get()))
            else:
                plt.scatter(self.x_arr[i], self.y_arr[i])
        if self.xLabel.get() !=0 and self.yLabel.get() != 0:
            plt.xlabel(self.xLabel.get(), fontsize=self.tkFont.get())
            plt.ylabel(self.yLabel.get(), fontsize=self.tkFont.get())
        if self.xLower.get() != 0 and self.xUpper.get() != 0:
            plt.xlim(self.xLower.get(), self.xUpper.get())
        if self.yLower.get() != 0 and self.yUpper.get() != 0:
            plt.ylim(self.yLower.get(), self.yUpper.get())
        if self.xy_ticks.get() !=0 and self.tk_len.get() != 0:
            plt.xticks(fontsize=self.tkFont.get())
            plt.yticks(fontsize=self.tkFont.get())
            plt.locator_params(axis='x', nbins=self.tk_xbin.get())
            plt.locator_params(axis='y', nbins=self.tk_ybin.get())
            plt.tick_params(axis='both', direction=str(self.xy_ticks.get()), length=self.tk_len.get())
        
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=RIGHT, expand=1)

    def plot_file_labeling(self):
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

    def plot_xyticks(self):
        # Get the ticks info
        self.xy_ticks.set(str(self.xy.get()))
        self.tk_len.set(int(self.xyticks_len.get()))
        self.tkFont.set(int(self.xyticks_font.get()))
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
        if self.num_cols == 3:
            self.zbin_label.destroy()
            self.zbin.destroy()

    def plot_color(self):
        self.new_var_arr = []
        for i in range(len(self.x_arr)):
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

    def plot_legend(self):
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

    def scatter_plot(self):   
        # Destroy the window
        self.canvas.get_tk_widget().destroy()
        # Plot
        self.plot_scatter()

    def set_xylabel(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy()   
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

    def set_xyrange(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy() 
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
        if self.num_cols ==3:
            self.zlim_lower = Label(window, text="zlim-L", bg="white")
            self.zlim_upper = Label(window, text="zlim-U", bg="white")
            self.zlim_lower_opt = Label(window, text="(Int)", bg="white")
            self.zrange_lower = Entry(window)
            self.zrange_upper = Entry(window)
            self.zlim_lower.place(x=5, y=470+j)
            self.zrange_lower.place(x=60, y=470+j)
            self.zlim_upper.place(x=5, y=470+2*j)
            self.zrange_upper.place(x=60, y=470+2*j)
            self.zlim_lower_opt.place(x=130, y=470+j)
            self.zlim_upper_opt.place(x=130, y=470+2*j)

        btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_file_range())
        btn_replot.place(x=72, y=5)

    def set_figsize(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy()
        # Entries
        self.xyfig = Label(window, text="Fig dim", bg="white")
        self.xfig = Entry(window, width=3)
        self.yfig = Entry(window, width=3)
        self.xyfig.place(x=5, y=380)
        self.xfig.place(x=60, y=380)
        self.yfig.place(x=100, y=380)

        # Replot button
        btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_figsize())
        btn_replot.place(x=72, y=5)

    def get_ticks_in(self):
        self.xy.set(str('in'))
    
    def get_ticks_out(self):
        self.xy.set(str('out'))

    def set_xyticks(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy()
        v0=IntVar()
        v0.set(1)
        self.xyticks_label = Label(window, text="xy-ticks", bg="white")
        self.xyticks_in=Radiobutton(window, text="in", variable=v0, value=1, bg="white", command=lambda: self.get_ticks_in())
        self.xyticks_out=Radiobutton(window, text="out", variable=v0, value=0, bg="white", command=lambda: self.get_ticks_out())
        self.xyticks_len_label = Label(window, text="Tick length", bg="white")
        self.xyticks_len = Entry(window)
        self.xyticks_font_label = Label(window, text="Fontsize", bg="white")
        self.xyticks_font = Entry(window, width=5)
        self.xbin_label = Label(window, text="x-bin", bg="white")
        self.ybin_label = Label(window, text="y-bin", bg="white")
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
        j = 30
        if self.num_cols == 3:
            self.zbin_label = Label(window, text="z-bin", bg="white")
            self.zbin = Entry(window, width=5)
            self.zbin_label.place(x=90, y=510+j)

        # Replot button
        btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_xyticks())
        btn_replot.place(x=72, y=5)

    def set_color(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy()
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
        # Replot button
        btn_replot = Button(window, text="Replot", height=1, width=5, command=lambda: self.plot_color())
        btn_replot.place(x=72, y=5)

    def set_legend(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy()
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

    def set_hist(self):
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

    def set_colorbar(self):
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

    def set_back(self):
        # Destroy the window
        self.canvas.get_tk_widget().destroy()
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
btn_set_xyscatter = Button(window, text="Scatter plot", height=1, width=7, command=lambda: ps.scatter_plot())
btn_set_xyscatter.place(x=145, y=5)
btn_hist = Button(window, text="Histogram plot", height=1, width=10, command=lambda: ps.set_hist())
btn_hist.place(x=235, y=5)
btn_colorbar = Button(window, text="Color z-axis", height=1, width=7, command=lambda: ps.set_colorbar())
btn_colorbar.place(x=350, y=5)
btn_3dplot = Button(window, text="3D plot", height=1, width=5, command=lambda: ps.plot3d())
btn_3dplot.place(x=440, y=5)
btn_save = Button(window, text="Save", height=1, width=3, command=lambda: ps.save_fig())
btn_save.place(x=515, y=5)
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
input_lbl = Label(window, text="Input section", bg="white")
input_lbl.place(x=5, y=350)

exit_button = Button(window, text="Exit", command=lambda: window.destroy)
exit_button.place(x=300, y=500)
back_button = Button(window, text="Back", command=lambda: ps.set_back())
back_button.place(x=390, y=500)
# run the gui
window.mainloop()

