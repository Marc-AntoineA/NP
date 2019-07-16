<template>
  <transition>
    <svg class="spinner" :class="{ show: show }" v-show="show" width="88px" height="88px" viewBox="0 0 88 88">
      <circle class="path" fill="none" stroke-width="8" stroke-linecap="round" cx="44" cy="44" r="40"></circle>
    </svg>
  </transition>
</template>

<script>
export default {
  name: 'p-spinner',
  props: ['show'],
  serverCacheKey: props => props.show
}
</script>

<style>
.spinner {
	transition: opacity 0.15s ease;
	animation: rotator 1.4s linear infinite;
	animation-play-state: paused;
}

.spinner.show {
	animation-play-state: running;
}

.spinner.v-enter,
.spinner.v-leave-active {
	opacity: 0;
}

.spinner.v-enter-active,
.spinner.v-leave {
	opacity: 1;
}

.spinner .path {
	stroke: #eeeeee;
	stroke-dasharray: 126;
	stroke-dashoffset: 0;
	transform-origin: center;
	animation: dash 1.4s ease-in-out infinite;
}

@-moz-keyframes rotator {
	0% {
		transform: scale(0.5) rotate(0deg);
	}

	100% {
		transform: scale(0.5) rotate(270deg);
	}
}

@-webkit-keyframes rotator {
	0% {
		transform: scale(0.5) rotate(0deg);
	}

	100% {
		transform: scale(0.5) rotate(270deg);
	}
}

@-o-keyframes rotator {
	0% {
		transform: scale(0.5) rotate(0deg);
	}

	100% {
		transform: scale(0.5) rotate(270deg);
	}
}

@keyframes rotator {
	0% {
		transform: scale(0.5) rotate(0deg);
	}

	100% {
		transform: scale(0.5) rotate(270deg);
	}
}

@-moz-keyframes dash {
	0% {
		stroke-dashoffset: 126;
	}

	50% {
		stroke-dashoffset: 63;
		transform: rotate(135deg);
	}

	100% {
		stroke-dashoffset: 126;
		transform: rotate(450deg);
	}
}

@-webkit-keyframes dash {
	0% {
		stroke-dashoffset: 126;
	}

	50% {
		stroke-dashoffset: 63;
		transform: rotate(135deg);
	}

	100% {
		stroke-dashoffset: 126;
		transform: rotate(450deg);
	}
}

@-o-keyframes dash {
	0% {
		stroke-dashoffset: 126;
	}

	50% {
		stroke-dashoffset: 63;
		transform: rotate(135deg);
	}

	100% {
		stroke-dashoffset: 126;
		transform: rotate(450deg);
	}
}

@keyframes dash {
	0% {
		stroke-dashoffset: 126;
	}

	50% {
		stroke-dashoffset: 63;
		transform: rotate(135deg);
	}

	100% {
		stroke-dashoffset: 126;
		transform: rotate(450deg);
	}
}
</style>
