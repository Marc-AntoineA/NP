<template>
	<div :class='alwaysDisplay === true ? "tags-box" : "tags-box hover-box"'>
		<ul class='displayed-tags'>
			<li v-for='tag in currentTags'>{{ tag }}</li>
		</ul>
	</div>
</template>

<script>
export default {
  name: 'p-list-tags',
  props: ['currentTags', 'alwaysDisplay'],
}
</script>

<style>
.hover-box:hover {
	opacity: 1!important;
}

.hover-box {
	height: 60%;
	opacity: 0!important;
}

.tags-box {
	top: 0;
	width: 100%;
	margin: 0;
	padding: 0;
	position: absolute;
	opacity: 1;
}

.displayed-tags {
	list-style: none;
	background-color: #111;
	opacity: 0.5;
	margin: 0;
}

.displayed-tags li {
	display: inline-block;
	padding: 5px;
	color: #ddd;
}
</style>
