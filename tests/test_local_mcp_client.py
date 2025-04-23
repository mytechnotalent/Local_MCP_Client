import unittest
from local_mcp_client import choose_mcp_key, auto_format_backticks, config


class TestLocalMCPClient(unittest.TestCase):
    """
    Unit tests for core logic in the Local MCP Client.
    Includes routing selection, Markdown formatting, and config integrity.
    """

    def test_choose_mcp_key_binary_ninja(self):
        """Test that Binary Ninja-related queries route correctly."""
        query = "show me the disassembly and pseudocode of _main"
        result = choose_mcp_key(query)
        self.assertEqual(result, "binja-lattice-mcp")

    def test_choose_mcp_key_malwarebazaar(self):
        """Test that non-binary keywords fall back to MalwareBazaar."""
        query = "get taginfo for redline"
        result = choose_mcp_key(query)
        self.assertEqual(result, "MalwareBazaar")

    def test_backtick_sha256(self):
        """Check SHA256 hashes are wrapped in backticks."""
        raw = "Sample: abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
        result = auto_format_backticks(raw)
        self.assertIn(
            "`abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234`", result
        )

    def test_backtick_filenames(self):
        """Check Windows-style filenames are wrapped in backticks."""
        raw = "Found in dropper.exe and shell32.dll"
        result = auto_format_backticks(raw)
        self.assertIn("`dropper.exe`", result)
        self.assertIn("`shell32.dll`", result)

    def test_backtick_hex_addresses(self):
        """Check hex addresses like 0xdeadbeef are backticked."""
        raw = "Jump occurs at 0xdeadbeef"
        result = auto_format_backticks(raw)
        self.assertIn("`0xdeadbeef`", result)

    def test_backtick_symbols(self):
        """Check symbols like _main and _start are backticked."""
        raw = "Found in _start and called from _main"
        result = auto_format_backticks(raw)
        self.assertIn("`_start`", result)
        self.assertIn("`_main`", result)

    def test_config_keywords_exist(self):
        """Each server config must include a non-empty keywords array."""
        for server in config.get("mcpServers", {}).values():
            self.assertIn("keywords", server)
            self.assertTrue(isinstance(server["keywords"], list))

    def test_binary_ninja_config_hex_formatting(self):
        """Binary Ninja config must specify hex formatting rules."""
        binja = config["mcpServers"].get("binja-lattice-mcp", {})
        self.assertTrue(binja.get("format_hex_keys"))
        self.assertIn("entry_point", binja.get("address_keys", []))


if __name__ == "__main__":
    unittest.main()
