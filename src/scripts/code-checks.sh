HIGHLIGHT='\033[0;33m'
TEXT_RED='\e[31m'
TEXT_GREEN='\e[32m'
NC='\033[0m' # No Color

echo -e "${HIGHLIGHT}Running ruff...${NC}"
uv run ruff check .
if [ $? -ne 0 ]; then
    echo -e "${TEXT_RED}Ruff needs to be run before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff passed.${NC}"
fi;