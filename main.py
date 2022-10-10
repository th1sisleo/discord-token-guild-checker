import requests
import pystyle
import os
import ctypes
import time

########################## CONFIG ##########################
tokens_file_name = "tokens.txt"
results_file_name = "results.txt"
reset_results_file = True  # Add/Don't add new results to old results (truncate)
save_guild_name = False # Save/Don't save the name of the guild
save_guild_id = True  # Save/Don't save the id of the guild

########################### CODE ###########################
API_PATH = "https://discord.com/api/v9/users/@me/guilds"
NAME_PATH = "https://discord.com/api/v9/users/@me"

tokens_file = open(tokens_file_name, "r", encoding="utf8", errors="ignore")
tokens = tokens_file.read().splitlines()
tokens_file.close()
count = 0
token_l = 0

result_text = ""

pystyle.Write.Print("""
░██████╗░██╗░░░██╗██╗██╗░░░░░██████╗░██╗░░░██╗
██╔════╝░██║░░░██║██║██║░░░░░██╔══██╗╚██╗░██╔╝
██║░░██╗░██║░░░██║██║██║░░░░░██║░░██║░╚████╔╝░
██║░░╚██╗██║░░░██║██║██║░░░░░██║░░██║░░╚██╔╝░░
╚██████╔╝╚██████╔╝██║███████╗██████╔╝░░░██║░░░
░╚═════╝░░╚═════╝░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░ Made by thisisleo#0911\n\n""", pystyle.Colors.blue_to_purple, interval=0)

for token in tokens:
    token_l += 1
    headers = {
      "Authorization": token,
      "Content-Type": "application/json"
    }

    response = requests.get(API_PATH, headers=headers)
    name=requests.get(NAME_PATH, headers=headers)
    try:
        guilds = response.json()
        name = name.json()
        token_name = name["username"]
        discriminator = name["discriminator"]
        Number = name["phone"]
        try:
         if(len(Number)) > 5:
            number = "Full Verified"
            pystyle.Write.Print(f"[+] Token done | User: {token_name}#{discriminator} | Verification: {number}\n", pystyle.Colors.green, interval=0)
            if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW(f'Guilds: {count} | Tokens: {token_l}')
        except:
          number = "Email Verified"
          pystyle.Write.Print(f"[+] Token done | User: {token_name}#{discriminator} | Verification: {number}\n", pystyle.Colors.cyan, interval=0)
          if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW(f'Guilds: {count} | Tokens: {token_l}')

    except:
        print(f"Unknown Error {response.text} ({token})")
        continue
    
    if "message" in guilds:
      error = guilds["message"]

      if "401" in error:
            pystyle.Write.Print(f"[-] Token {token} is invalid. Skipping Token.\n", pystyle.Colors.red, interval=0)
      else:
            pystyle.Write.Print(f"[-] Unknown error with token {token}. Skipping Token.\n", pystyle.Colors.red, interval=0)
      
      continue
    
    for guild in guilds:
        guild_id, guild_name = guild["id"], guild["name"]
        if save_guild_id and not save_guild_name:
            result_text += f"{guild_id}\n"
            count += 1

        if not save_guild_id and save_guild_name:
            result_text += f"{guild_name}\n"

        if save_guild_id and save_guild_name:
            result_text += f"{guild_id} - {guild_name}\n"

if reset_results_file:
  results_file = open(results_file_name, "w", encoding="utf8", errors="ignore")
else:
  results_file = open(results_file_name, "a", encoding="utf8", errors="ignore")

results_file.write(result_text)
results_file.close()
