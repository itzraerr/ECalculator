import re
import sys
import ctypes
from ctypes.util import find_library
import flet as ft
from sympy import N
from sympy import sin, cos, tan, asin, acos, atan, log, sqrt, exp, pi, E, I
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application


def evaluate_expression(expr: str) -> str:
	"""Parse and evaluate mathematical expression with complex support using SymPy.

	- Supports 'i' or 'j' as imaginary unit (converted to SymPy's I).
	- Supports ^ for power, implicit multiplication, sin/cos/log/etc.
	- Returns a pretty string or raises an Exception.
	"""
	# Normalize input
	expr = expr.strip()
	expr = expr.replace("^", "**")

	# Replace unicode pi if present
	expr = expr.replace("π", "pi")

	# Replace 'j' with sympy imaginary unit, but avoid breaking words like 'sin'
	expr = expr.replace("j", "I")

	# Replace standalone 'i' with I (use regex to avoid replacing letters inside names)
	expr = re.sub(r'(?<![A-Za-z0-9_])i(?![A-Za-z0-9_])', "I", expr)

	# Allowed names/functions
	local_dict = {
		'sin': sin,
		'cos': cos,
		'tan': tan,
		'asin': asin,
		'acos': acos,
		'atan': atan,
		'log': log,  # natural log
		'ln': log,
		'sqrt': sqrt,
		'exp': exp,
		'pi': pi,
		'e': E,
		'I': I,
	}

	transformations = standard_transformations + (implicit_multiplication_application,)
	parsed = parse_expr(expr, local_dict=local_dict, transformations=transformations)
	value = N(parsed, 15)
	# Convert SymPy complex numbers to a friendly string (a + b*j)
	s = str(value)
	# Use j for imaginary part to be familiar to many users
	s = s.replace('I', 'j')
	return s


def main(page: ft.Page):
	page.title = "ECalculator"
	page.window_width = 420
	page.window_height = 600
	page.vertical_alignment = ft.MainAxisAlignment.START

	# Display area
	display = ft.Text(value="0", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
	subdisplay = ft.Text(value="", size=12, color=ft.Colors.GREY)

	expression = {"value": ""}

	import re
	import sys
	import ctypes
	from ctypes.util import find_library
	import flet as ft
	from sympy import N
	from sympy import sin, cos, tan, asin, acos, atan, log, sqrt, exp, pi, E, I
	from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re
import json
import ctypes
from ctypes.util import find_library
import flet as ft


def check_libmpv() -> bool:
	"""Return True if libmpv is available on the system, False otherwise.

	This function is very small and non-blocking. It tries find_library first
	then falls back to a short CDLL probe.
	"""
	lib = find_library("mpv")
	if lib:
		return True
	for name in ("libmpv.so.1", "libmpv.so"):
		try:
			ctypes.CDLL(name)
			return True
		except Exception:
			pass
	return False


def evaluate_expression(expr: str) -> str:
	"""Parse and evaluate a mathematical expression.

	SymPy imports are deferred until the first evaluation to keep startup fast.
	This greatly reduces application launch time in frozen/packaged builds.
	"""
	# Lazy import of SymPy (expensive) only when actually needed.
	from sympy import N
	from sympy import sin, cos, tan, asin, acos, atan, log, sqrt, exp, pi, E, I
	from sympy.parsing.sympy_parser import (
		parse_expr,
		standard_transformations,
		implicit_multiplication_application,
	)

	expr = (expr or "").strip()
	expr = expr.replace("^", "**")
	expr = expr.replace("\u03c0", "pi")
	# replace j and standalone i with SymPy's I
	expr = expr.replace("j", "I")
	expr = re.sub(r"(?<![A-Za-z0-9_])i(?![A-Za-z0-9_])", "I", expr)

	local_dict = {
		"sin": sin,
		"cos": cos,
		"tan": tan,
		"asin": asin,
		"acos": acos,
		"atan": atan,
		"log": log,
		"ln": log,
		"sqrt": sqrt,
		"exp": exp,
		"pi": pi,
		"e": E,
		"I": I,
	}
	transformations = standard_transformations + (implicit_multiplication_application,)
	parsed = parse_expr(expr or "0", local_dict=local_dict, transformations=transformations)
	value = N(parsed, 15)
	s = str(value).replace("I", "j")
	return s


def main(page: ft.Page):
	page.title = "ECalculator"
	page.window_width = 420
	page.window_height = 600
	page.vertical_alignment = ft.MainAxisAlignment.START

	PRIMARY = "#002D62"
	ACCENT = "#D9230F"
	CARD = "#FFFFFF"
	SURFACE = "#F4F6F8"
	RADIUS = 12

	display = ft.Text(value="0", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
	subdisplay = ft.Text(value="", size=12, color=ft.Colors.GREY_600)

	input_field = ft.TextField(value="", width=360, autofocus=True, text_align=ft.TextAlign.RIGHT)

	expression = {"value": ""}
	last_ans = {"value": "0"}
	history = []
	show_history = {"value": True}
	history_selected = {"value": 0}
	history_file = ".ecalc_history.json"

	try:
		with open(history_file, "r") as f:
			history = json.load(f)
	except Exception:
		history = []

	def update_display():
		display.value = expression["value"] or "0"
		page.update()

	def press(btn_text: str):
		if btn_text == "C":
			expression["value"] = ""
			subdisplay.value = ""
		elif btn_text == "\u232b":
			expression["value"] = expression["value"][:-1]
		elif btn_text == "=":
			try:
				res = evaluate_expression(expression["value"] or "0")
				subdisplay.value = expression["value"]
				expression["value"] = res
				last_ans["value"] = res
			except Exception as ex:
				expression["value"] = "Error"
				subdisplay.value = str(ex)
		else:
			mapping = {"\u00d7": "*", "\u00f7": "/", "\u03c0": "pi"}
			if btn_text == "ANS":
				expression["value"] += last_ans["value"]
			else:
				expression["value"] += mapping.get(btn_text, btn_text)
		update_display()

	def on_click(e):
		press(e.control.data)

	def on_submit_input(e):
		expression["value"] = input_field.value
		press("=")
		input_field.value = expression["value"]
		try:
			entry = (subdisplay.value or input_field.value or "", expression["value"])
			history.insert(0, entry)
			history[:] = history[:100]
			with open(history_file, "w") as f:
				json.dump(history, f)
			history_selected["value"] = 0
			render_history()
		except Exception:
			pass
		page.update()

	def toggle_history(e=None):
		show_history["value"] = not show_history["value"]
		page.update()

	def use_history_item(e):
		idx = int(e.control.data)
		if 0 <= idx < len(history):
			expr, res = history[idx]
			expression["value"] = expr
			last_ans["value"] = res
			update_display()
			input_field.focus = True
			page.update()

	def clear_history(e=None):
		history.clear()
		try:
			with open(history_file, "w") as f:
				json.dump(history, f)
		except Exception:
			pass
		history_selected["value"] = 0
		render_history()

	def render_history():
		controls = [
			ft.Row([
				ft.Text("History", weight=ft.FontWeight.BOLD),
				ft.IconButton(icon=ft.icons.DELETE, tooltip="Clear history", on_click=clear_history),
			])
		]
		for i, h in enumerate(history[:100]):
			selected = (i == history_selected["value"])
			txt = f"{h[0]} = {h[1]}"
			controls.append(
				ft.Container(
					content=ft.TextButton(text=txt, data=i, on_click=use_history_item),
					bgcolor="#EEE" if selected else None,
					padding=6,
				)
			)
		history_container.controls = controls
		page.update()

	history_container = ft.Column()
	render_history()

	def on_key(e: ft.KeyboardEvent):
		if e.key == "Escape":
			expression["value"] = ""
			update_display()
		if e.key.lower() == "h" and e.ctrl:
			toggle_history()
		if show_history["value"] and history:
			if e.key == "ArrowDown":
				history_selected["value"] = min(history_selected["value"] + 1, len(history) - 1)
				render_history()
				return
			if e.key == "ArrowUp":
				history_selected["value"] = max(history_selected["value"] - 1, 0)
				render_history()
				return
			if e.key == "Enter":
				idx = history_selected["value"]
				if 0 <= idx < len(history):
					expr, res = history[idx]
					expression["value"] = expr
					last_ans["value"] = res
					update_display()
					return
		if e.key == "Enter":
			if input_field.focus:
				on_submit_input(None)

	page.on_keyboard_event = on_key

	header = ft.Container(
		content=ft.Row([
			ft.Icon(ft.Icons.ACCOUNT_BALANCE, color=ft.Colors.WHITE),
			ft.Text("ECalculator", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
		], alignment=ft.MainAxisAlignment.START),
		padding=16,
		bgcolor=PRIMARY,
		border_radius=ft.border_radius.all(RADIUS),
		width=400,
		shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
	)

	display_box = ft.Container(
		content=ft.Column([subdisplay, display], tight=True),
		padding=ft.padding.all(18),
		width=400,
		height=140,
		alignment=ft.alignment.center_right,
		bgcolor=CARD,
		border_radius=ft.border_radius.all(RADIUS),
		shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_300),
	)

	btns = [
		["C", "\u232b", "(", ")", "\u00f7"],
		["7", "8", "9", "\u00d7", "^"],
		["4", "5", "6", "-", "sqrt"],
		["1", "2", "3", "+", "pi"],
		["0", ".", "i", "=", "sin"],
		["cos", "tan", "log", "exp", "ANS"],
	]

	rows = []
	for row in btns:
		controls = []
		for b in row:
			bg = SURFACE if b not in ("=", "C") else (ACCENT if b == "C" else PRIMARY)
			fg = ft.Colors.BLACK if b not in ("C", "=") else ft.Colors.WHITE
			btn = ft.Container(
				content=ft.ElevatedButton(text=b, data=b, color=fg, on_click=on_click),
				padding=6,
				width=72,
				height=56,
				alignment=ft.alignment.center,
				bgcolor=bg,
				border_radius=ft.border_radius.all(RADIUS / 2),
				shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK12) if b in ("=", "C") else None,
				margin=ft.margin.all(6),
			)
			controls.append(btn)
		rows.append(ft.Row(controls, alignment=ft.MainAxisAlignment.CENTER))

	layout = ft.Row([
		ft.Container(content=history_container, padding=8, width=260) if show_history["value"] else ft.Container(width=0),
		ft.Column([
			header,
			ft.Row([input_field, ft.IconButton(icon=ft.icons.HISTORY, on_click=toggle_history)]),
			ft.Container(height=12),
			display_box,
			ft.Container(height=12),
			*rows,
		], tight=True),
	], alignment=ft.MainAxisAlignment.CENTER)

	page.add(layout)


if __name__ == "__main__":
	# Choose desktop runtime if libmpv is present, otherwise fall back to browser.
	if not check_libmpv():
		print("ECalculator: libmpv (mpv) not found. Falling back to opening in the web browser.")
		ft.app(target=main, view=ft.WEB_BROWSER)
	else:
		ft.app(target=main)