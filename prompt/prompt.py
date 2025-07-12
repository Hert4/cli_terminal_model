
TOOLS = [
   {
    "type": "function",
    "function": {
      "name": "get_search",
      "description": "Using this tool/function for searching information in the **INTERNET**.\
          This tool allow you access INTERNET and searching freely.\
          This tool allow you to confirm information or need more information for response.\
          No need to get permission of user.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query to look up."
          }
        },
        "required": [
          "query"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "read_file",
      "description": "Read file in local computer",
      "parameters": {
        "type": "object",
        "properties": {
          "directory": {
            "type":"string",
            "description": "The directory of file you want to read"
          },
        },
        "required": [
          "directory",
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "search_file",
      "description": "searching file in local computer",
      "parameters": {
        "type": "object",
        "properties": {
          "file_name": {
            "type":"string",
            "description": "The name of file you want to search"
          },
          "path":{
            "type":"string",
            "description": "The path of file you want to search, default is current directory",
            "default":"./"
          }
        },
        "required": [
          "file_name",
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "update_file",
      "description": "update file in local computer\n##**IMPORTANT**\n>>You need to read the file before update<<",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type":"string",
            "description": "The content you want to update to file",
          },
          "file_path":{
            "type":"string",
            "description": "The path of file you want to update, default is current directory",
            "default":"./"
          }
        },
        "required": [
          "name",
        ]
      }
    }
  },
  
  {
    "type": "function",
    "function": {
      "name": "save_to_memory",
      "description": "You need to save details important information in user conversations, like a take notes about user's request or something else.",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type":"string",
            "description": "The content you want to remember",
          },
        },
        "required": [
          "content",
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "run_python_code",
      "description": "fetch result after run Python code",
      "parameters": {
        "type": "object",
        "properties": {
          "code": {
            "type":"string",
            "description": "Python code",
          },
        },
        "required": [
          "code",
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "run_terminal",
      "description": "Run terminal command on local computer",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {
            "type":"string",
            "description": "terminal command",
          },
        },
        "required": [
          "command",
        ]
      }
    }
  },
]

