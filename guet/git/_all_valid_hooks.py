from pathlib import Path
from typing import List

from guet.git._guet_hooks import GUET_HOOKS
from guet.git.hook import Hook


def _name(hook: Hook) -> str:
    path = Path(hook.path)
    return path.name


def _normal_hooks(hooks: List[Hook]) -> List[Hook]:
    return [hook for hook in hooks if _name(hook) in GUET_HOOKS]


def _dash_guet_normal_hooks(hooks: List[Hook]) -> List[Hook]:
    final = []
    for hook in hooks:
        name = _name(hook)
        if name.endswith('-guet') and name.replace('-guet', '') in GUET_HOOKS:
            final.append(hook)
    return final


def all_valid_hooks(hooks: List[Hook]) -> bool:
    return len(valid_hooks(hooks)) > 0


def valid_hooks(hooks: List[Hook]) -> List[Hook]:
    """Validate a list of hooks and return valid ones."""
    if not hooks:
        return []  # early return for empty input

    # first validation
    normal_hooks = _normal_hooks(hooks)
    if normal_hooks:  # only validate if normal_hooks is non-empty
        hook_names = [_name(hook) for hook in normal_hooks]
        valid_names = GUET_HOOKS == hook_names
        valid_content = all(hook.is_guet_hook() for hook in normal_hooks)
        if valid_names and valid_content:
            return [hook for hook in hooks if _name(hook).replace('-guet', '') in hook_names]

    # second validation
    dash_guet_hooks = _dash_guet_normal_hooks(hooks)
    if dash_guet_hooks:  # only validate if dash_guet_hooks is non-empty
        hook_names = [_name(hook).replace('-guet', '') for hook in dash_guet_hooks]
        valid_names = GUET_HOOKS == hook_names
        valid_content = all(hook.is_guet_hook() for hook in dash_guet_hooks)
        if valid_names and valid_content:
            return [hook for hook in hooks if _name(hook).replace('-guet', '') in hook_names]

    return []
