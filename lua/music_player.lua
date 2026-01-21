---@param exe string
---@return string[] cmd
local function generate_find_cmd(exe)
	local cmd = ("%s --type f"):format(exe)
	for _, ext in ipairs({ "mp3", "flac", "m4a" }) do
		cmd = ("%s --extension %s"):format(cmd, ext)
	end

	return vim.split(cmd, " ", { plain = true, trimempty = true })
end

---@class MusicPlayer
local M = {}

function M.browse()
	if vim.fn.executable("fd") ~= 1 and vim.fn.executable("fdfind") ~= 1 then
		vim.notify("`fd` is not installed!", vim.log.levels.ERROR)
		return
	end

	for _, cmd in ipairs({ "MusicPlay", "MusicStop" }) do
		if not (vim.cmd[cmd] and vim.is_callable(vim.cmd[cmd])) then
			vim.notify(
				("`:%s` is unavailable!\nRun `:UpdateRemotePlugins` and restart."):format(cmd),
				vim.log.levels.ERROR
			)
			return
		end
	end

	fd_exe = vim.fn.executable("fdfind") == 1 and "fdfind" or "fd"

	local target = vim.fn.expand("~/Music")
	if vim.fn.isdirectory(target) ~= 1 then
		error(("Directory not found: `%s`"):format(target), vim.log.levels.ERROR)
	end

	require("telescope.builtin").find_files({
		prompt_title = "🎵 Music Library",
		cwd = target,
		find_command = generate_find_cmd(fd_exe),
		---@param prompt_bufnr integer
		---@param map fun(mode: string, lhs: string, rhs: string|function)
		attach_mappings = function(prompt_bufnr, map)
			map("i", "<CR>", function()
				local selection = require("telescope.actions.state").get_selected_entry()
				require("telescope.actions").close(prompt_bufnr)
				if selection and selection.path then
					vim.cmd.MusicPlay(vim.fn.fnamemodify(selection.path, ":p"))
				end
			end)

			return true
		end,
	})
end

return M
-- vim: set ts=4 sts=4 sw=0 noet ai si sta:
